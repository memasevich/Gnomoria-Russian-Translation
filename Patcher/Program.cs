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
            string gameDir = @"D:\steam\steamapps\common\Gnomoria";
            string exePath = Path.Combine(gameDir, "Gnomoria.exe");
            string backupPath = Path.Combine(gameDir, "Gnomoria.exe.backup");
            string translatorDll = @"C:\Users\Lecoo\projects\GnomoriaTranslator\Translator\bin\Release\net472\Translator.dll";

            var resolver = new DefaultAssemblyResolver();
            resolver.AddSearchDirectory(gameDir); // Здесь он найдет gnomorialib.dll

            var readerParams = new ReaderParameters { AssemblyResolver = resolver };
            
            using (var module = ModuleDefinition.ReadModule(backupPath, readerParams))
            {
                var entry = module.EntryPoint;
                var transAsm = AssemblyDefinition.ReadAssembly(translatorDll);
                var initMethod = transAsm.MainModule.Types.First(t => t.Name == "Hook").Methods.First(m => m.Name == "Init");
                var initRef = module.ImportReference(initMethod);

                var il = entry.Body.GetILProcessor();
                il.InsertBefore(entry.Body.Instructions.First(), il.Create(OpCodes.Call, initRef));

                module.Write(exePath);
                Console.WriteLine("Patcher: Success. Size: " + new FileInfo(exePath).Length);
            }
        }
    }
}
