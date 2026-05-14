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
            string translatorDll = "Translator.dll";

            if (!File.Exists(exePath))
            {
                Console.WriteLine("Gnomoria.exe not found at " + exePath);
                return;
            }

            if (!File.Exists(backupPath))
            {
                File.Copy(exePath, backupPath);
                Console.WriteLine("Backup created.");
            }

            var resolver = new DefaultAssemblyResolver();
            resolver.AddSearchDirectory(gameDir);
            resolver.AddSearchDirectory(Path.Combine(gameDir, "x86")); // Optional
            resolver.AddSearchDirectory(Directory.GetCurrentDirectory());
            resolver.AddSearchDirectory(@"C:\Windows\Microsoft.NET\assembly\GAC_32\Microsoft.Xna.Framework\v4.0_4.0.0.0__842cf8be1de50553");
            resolver.AddSearchDirectory(@"C:\Windows\Microsoft.NET\assembly\GAC_32\Microsoft.Xna.Framework.Graphics\v4.0_4.0.0.0__842cf8be1de50553");
            resolver.AddSearchDirectory(@"C:\Windows\Microsoft.NET\assembly\GAC_32\Microsoft.Xna.Framework.Game\v4.0_4.0.0.0__842cf8be1de50553");

            var parameters = new ReaderParameters { AssemblyResolver = resolver };
            
            try 
            {
                using (var module = ModuleDefinition.ReadModule(backupPath, parameters))
                {
                    var mainMethod = module.EntryPoint;
                    if (mainMethod == null)
                    {
                        Console.WriteLine("Could not find EntryPoint.");
                        return;
                    }

                    Console.WriteLine("Found EntryPoint method: " + mainMethod.FullName + ". Injecting...");

                    // Load Translator assembly to get reference to Hook.Init
                    string transDllPath = Path.Combine(@"C:\Users\Lecoo\projects\GnomoriaTranslator\Translator\bin\Debug\net472", translatorDll);
                    var translatorRefAsm = AssemblyDefinition.ReadAssembly(transDllPath);
                    var hookType = translatorRefAsm.MainModule.Types.First(t => t.Name == "Hook");
                    var initMethod = hookType.Methods.First(m => m.Name == "Init");

                    var initRef = module.ImportReference(initMethod);

                    var ilProcessor = mainMethod.Body.GetILProcessor();
                    var firstInstruction = mainMethod.Body.Instructions.First();
                    
                    var callInstruction = Instruction.Create(OpCodes.Call, initRef);
                    ilProcessor.InsertBefore(firstInstruction, callInstruction);

                    module.Write(exePath);
                    Console.WriteLine("Injection successful!");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine("Error during injection: " + ex.Message);
            }
        }
    }
}
