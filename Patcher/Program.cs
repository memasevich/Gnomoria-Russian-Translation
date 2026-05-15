using System;
using System.IO;
using System.Linq;
using Mono.Cecil;
using Mono.Cecil.Cil;

namespace Patcher
{
    class Program
    {
        static void Main(string[] args)
        {
            try 
            {
                Console.WriteLine("--- Gnomoria Russian Patcher v4.0 ---");
                
                // Ищем файлы в текущей папке (где лежит патчер)
                string currentDir = AppDomain.CurrentDomain.BaseDirectory;
                string exePath = Path.Combine(currentDir, "Gnomoria.exe");
                string backupPath = Path.Combine(currentDir, "Gnomoria.exe.backup");
                string translatorDll = Path.Combine(currentDir, "Translator.dll");

                Console.WriteLine("Current dir: " + currentDir);

                if (!File.Exists(exePath)) {
                    Console.WriteLine("ERROR: Gnomoria.exe not found in " + currentDir);
                    return;
                }

                if (!File.Exists(translatorDll)) {
                    Console.WriteLine("ERROR: Translator.dll not found in " + currentDir);
                    return;
                }

                // Делаем бэкап если его нет
                if (!File.Exists(backupPath)) {
                    File.Copy(exePath, backupPath);
                    Console.WriteLine("Backup created: Gnomoria.exe.backup");
                }

                var resolver = new DefaultAssemblyResolver();
                resolver.AddSearchDirectory(currentDir);

                Console.WriteLine("Reading " + backupPath + "...");
                using (var module = ModuleDefinition.ReadModule(backupPath, new ReaderParameters { AssemblyResolver = resolver, ReadWrite = true }))
                {
                    var entry = module.EntryPoint;
                    if (entry == null) {
                        Console.WriteLine("ERROR: Could not find EntryPoint in Gnomoria.exe");
                        return;
                    }

                    Console.WriteLine("Injecting Hook.Init() into " + entry.FullName);
                    
                    var translatorAsm = AssemblyDefinition.ReadAssembly(translatorDll);
                    var hookType = translatorAsm.MainModule.Types.FirstOrDefault(t => t.Name == "Hook");
                    if (hookType == null) {
                        Console.WriteLine("ERROR: Could not find Hook class in Translator.dll");
                        return;
                    }

                    var initMethod = hookType.Methods.FirstOrDefault(m => m.Name == "Init");
                    var initRef = module.ImportReference(initMethod);

                    var il = entry.Body.GetILProcessor();
                    il.InsertBefore(entry.Body.Instructions.First(), Instruction.Create(OpCodes.Call, initRef));

                    Console.WriteLine("Writing patched EXE...");
                    module.Write(exePath);
                    Console.WriteLine("SUCCESS! Gnomoria.exe is now patched.");
                    Console.WriteLine("Patched file size: " + new FileInfo(exePath).Length);
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("CRITICAL ERROR: " + ex.ToString());
            }
            
            // Даем время прочитать вывод если запустили руками
            System.Threading.Thread.Sleep(2000);
        }
    }
}
