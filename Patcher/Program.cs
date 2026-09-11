// Gnomoria Russian Translation Patcher
// Developer: memasevich

using System;
using System.IO;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

namespace GnomoriaTranslator.Patcher
{
    internal class Program
    {
        private const string Version = "4.1.0";

        static int Main(string[] args)
        {
            Console.Title = "Gnomoria Russian Translation Patcher v" + Version;
            Console.ForegroundColor = ConsoleColor.Cyan;
            Console.WriteLine("==================================================");
            Console.WriteLine("    Gnomoria Russian Translation Patcher v" + Version);
            Console.WriteLine("    Developer: memasevich");
            Console.WriteLine("==================================================");
            Console.ResetColor();
            Console.WriteLine();

            string baseDir = AppDomain.CurrentDomain.BaseDirectory;
            bool isRestore = false;
            bool noWait = false;

            foreach (var rawArg in args)
            {
                if (string.IsNullOrWhiteSpace(rawArg)) continue;
                string arg = rawArg.Trim('"', '\'', ' ');

                if (arg.Equals("--restore", StringComparison.OrdinalIgnoreCase) ||
                    arg.Equals("-r", StringComparison.OrdinalIgnoreCase) ||
                    arg.Equals("--uninstall", StringComparison.OrdinalIgnoreCase) ||
                    arg.Equals("-u", StringComparison.OrdinalIgnoreCase))
                {
                    isRestore = true;
                    continue;
                }

                if (arg.Equals("--no-wait", StringComparison.OrdinalIgnoreCase) ||
                    arg.Equals("--no-pause", StringComparison.OrdinalIgnoreCase) ||
                    arg.Equals("-q", StringComparison.OrdinalIgnoreCase))
                {
                    noWait = true;
                    continue;
                }

                string dirCandidate = arg.TrimEnd('\\', '/');
                if (Directory.Exists(dirCandidate))
                {
                    baseDir = Path.GetFullPath(dirCandidate);
                }
            }

            string exePath = Path.Combine(baseDir, "Gnomoria.exe");
            string backupPath = Path.Combine(baseDir, "Gnomoria.exe.backup");
            string translatorDll = Path.Combine(baseDir, "Translator.dll");

            if (isRestore)
            {
                return RestoreBackup(exePath, backupPath, noWait);
            }

            if (!File.Exists(exePath))
            {
                PrintError("Gnomoria.exe не найден в директории: " + baseDir);
                WaitExit(noWait);
                return 1;
            }

            if (!File.Exists(translatorDll))
            {
                PrintError("Translator.dll не найден в директории: " + baseDir);
                WaitExit(noWait);
                return 1;
            }

            try
            {
                // Создаем бэкап если его нет
                if (!File.Exists(backupPath))
                {
                    Console.WriteLine("[*] Создание резервной копии: Gnomoria.exe.backup...");
                    File.Copy(exePath, backupPath, false);
                    Console.ForegroundColor = ConsoleColor.Green;
                    Console.WriteLine("[+] Резервная копия успешно создана.");
                    Console.ResetColor();
                }
                else
                {
                    Console.WriteLine("[i] Резервная копия уже существует (Gnomoria.exe.backup).");
                }

                var resolver = new DefaultAssemblyResolver();
                resolver.AddSearchDirectory(baseDir);

                var readerParams = new ReaderParameters
                {
                    AssemblyResolver = resolver,
                    ReadWrite = false
                };

                Console.WriteLine("[*] Чтение Gnomoria.exe в память...");
                byte[] exeBytes = File.ReadAllBytes(exePath);

                using (var stream = new MemoryStream(exeBytes))
                using (var module = ModuleDefinition.ReadModule(stream, readerParams))
                {
                    var entryPoint = module.EntryPoint;
                    if (entryPoint == null)
                    {
                        PrintError("Не удалось найти EntryPoint (точку входа) в Gnomoria.exe.");
                        WaitExit(noWait);
                        return 1;
                    }

                    // Проверяем, внедрен ли уже хук Translator
                    bool alreadyInjected = entryPoint.Body.Instructions.Any(i =>
                        i.OpCode == OpCodes.Call &&
                        i.Operand is MethodReference mr &&
                        mr.DeclaringType.FullName.Contains("Translator"));

                    if (alreadyInjected)
                    {
                        Console.ForegroundColor = ConsoleColor.Yellow;
                        Console.WriteLine("[!] Gnomoria.exe уже пропатчен русификатором.");
                        Console.ResetColor();
                        EnableLargeAddressAware(exePath);
                        WaitExit(noWait);
                        return 0;
                    }

                    // Проверяем наличие GnomoriaOptimizer - если он есть, не ломаем его!
                    bool hasOptimizer = entryPoint.Body.Instructions.Any(i =>
                        i.OpCode == OpCodes.Call &&
                        i.Operand is MethodReference mr &&
                        mr.DeclaringType.FullName.Contains("GnomoriaOptimizer"));

                    if (hasOptimizer)
                    {
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        Console.WriteLine("[i] Обнаружен GnomoriaOptimizer в точке входа. Совместимость сохраняется.");
                        Console.ResetColor();
                    }

                    using (module)
                    {
                        using (var translatorAsm = AssemblyDefinition.ReadAssembly(translatorDll))
                        {
                            var hookType = translatorAsm.MainModule.Types.FirstOrDefault(t => t.FullName == "GnomoriaTranslator.Hook" || t.Name == "Hook");
                            if (hookType == null)
                            {
                                PrintError("Класс Hook не найден в Translator.dll.");
                                WaitExit(noWait);
                                return 1;
                            }

                            var initMethod = hookType.Methods.FirstOrDefault(m => m.Name == "Init");
                            if (initMethod == null)
                            {
                                PrintError("Метод Init() не найден в Hook.");
                                WaitExit(noWait);
                                return 1;
                            }

                            var importedInit = module.ImportReference(initMethod);
                            var il = entryPoint.Body.GetILProcessor();
                            var firstInstruction = entryPoint.Body.Instructions[0];

                            il.InsertBefore(firstInstruction, Instruction.Create(OpCodes.Call, importedInit));
                        }

                        Console.WriteLine("[*] Запись изменений в Gnomoria.exe...");
                        module.Write(exePath);
                    }
                }

                EnableLargeAddressAware(exePath);

                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine();
                Console.WriteLine("==================================================");
                Console.WriteLine("[+] УСПЕХ! Gnomoria.exe успешно пропатчен русификатором.");
                Console.WriteLine("    Русский перевод и 4GB (LAA) готовы к работе.");
                Console.WriteLine("==================================================");
                Console.ResetColor();
            }
            catch (Exception ex)
            {
                PrintError("Критическая ошибка при патчинге: " + ex.Message);
                Console.WriteLine(ex.ToString());
                WaitExit(noWait);
                return 1;
            }

            WaitExit(noWait);
            return 0;
        }

        private static int RestoreBackup(string exePath, string backupPath, bool noWait)
        {
            if (!File.Exists(backupPath))
            {
                PrintError("Резервная копия Gnomoria.exe.backup не найдена: " + backupPath);
                WaitExit(noWait);
                return 1;
            }

            try
            {
                Console.WriteLine("[*] Восстановление оригинального Gnomoria.exe из бэкапа...");
                File.Copy(backupPath, exePath, true);
                Console.ForegroundColor = ConsoleColor.Green;
                Console.WriteLine("[+] Игра успешно восстановлена в исходное состояние.");
                Console.ResetColor();
            }
            catch (Exception ex)
            {
                PrintError("Ошибка при восстановлении: " + ex.Message);
                WaitExit(noWait);
                return 1;
            }

            WaitExit(noWait);
            return 0;
        }

        public static void EnableLargeAddressAware(string path)
        {
            try
            {
                using (var fs = new FileStream(path, FileMode.Open, FileAccess.ReadWrite))
                using (var br = new BinaryReader(fs))
                using (var bw = new BinaryWriter(fs))
                {
                    fs.Seek(0x3C, SeekOrigin.Begin);
                    int peOffset = br.ReadInt32();

                    long characteristicsOffset = peOffset + 4 + 18;
                    fs.Seek(characteristicsOffset, SeekOrigin.Begin);
                    ushort characteristics = br.ReadUInt16();

                    const ushort IMAGE_FILE_LARGE_ADDRESS_AWARE = 0x0020;
                    if ((characteristics & IMAGE_FILE_LARGE_ADDRESS_AWARE) == 0)
                    {
                        characteristics |= IMAGE_FILE_LARGE_ADDRESS_AWARE;
                        fs.Seek(characteristicsOffset, SeekOrigin.Begin);
                        bw.Write(characteristics);
                        Console.ForegroundColor = ConsoleColor.Cyan;
                        Console.WriteLine("[+] Активирован флаг Large Address Aware (LAA, 4GB ОЗУ).");
                        Console.ResetColor();
                    }
                    else
                    {
                        Console.WriteLine("[i] Флаг Large Address Aware (4GB ОЗУ) уже активен.");
                    }
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("[!] Предупреждение: Не удалось установить флаг LAA: " + ex.Message);
            }
        }

        private static void PrintError(string msg)
        {
            Console.ForegroundColor = ConsoleColor.Red;
            Console.WriteLine("[ERROR] " + msg);
            Console.ResetColor();
        }

        private static void WaitExit(bool noWait)
        {
            if (noWait) return;
            if (Environment.UserInteractive && !Console.IsInputRedirected)
            {
                Console.WriteLine();
                Console.WriteLine("Нажмите любую клавишу для выхода...");
                try { Console.ReadKey(); } catch { }
            }
        }
    }
}
