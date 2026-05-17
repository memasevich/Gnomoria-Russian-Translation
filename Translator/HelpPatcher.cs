using System;
using System.IO;
using System.Collections.Generic;
using System.Text;
using HarmonyLib;

namespace GnomoriaTranslator
{
    public static class HelpPatcher
    {
        public static void Patch(Harmony harmony)
        {
            try
            {
                // Загружаем сборку gnomorialib.dll, если она еще не загружена в текущем домене
                System.Reflection.Assembly gnomorialib = null;
                foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
                {
                    if (asm.GetName().Name == "gnomorialib")
                    {
                        gnomorialib = asm;
                        break;
                    }
                }
                if (gnomorialib == null)
                {
                    try
                    {
                        gnomorialib = System.Reflection.Assembly.LoadFrom("gnomorialib.dll");
                    }
                    catch { }
                }

                // Ищем класс GameEntityManager в Gnomoria.exe
                Type entityManagerType = null;
                foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
                {
                    entityManagerType = asm.GetType("Game.GameEntityManager");
                    if (entityManagerType != null) break;
                }

                if (entityManagerType != null)
                {
                    Hook.Log("Found GameEntityManager type! Patching get_HelpTopics...");
                    var method = entityManagerType.GetMethod("get_HelpTopics", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.NonPublic | System.Reflection.BindingFlags.Instance | System.Reflection.BindingFlags.Static);
                    if (method != null)
                    {
                        harmony.Patch(method, postfix: new HarmonyMethod(typeof(HelpPatcher), "Postfix"));
                        Hook.Log("Successfully patched get_HelpTopics!");
                    }
                    else
                    {
                        Hook.Log("ERROR: get_HelpTopics method not found in GameEntityManager!");
                    }
                }
                else
                {
                    Hook.Log("ERROR: GameEntityManager type not found!");
                }
            }
            catch (Exception ex)
            {
                Hook.Log("HelpPatcher Patch Error: " + ex.ToString());
            }
        }

        private static HashSet<GameLibrary.HelpTopic> translatedTopics = new HashSet<GameLibrary.HelpTopic>();

        public static void Postfix(GameLibrary.HelpTopic[] __result)
        {
            if (__result == null) return;

            try
            {
                foreach (var topic in __result)
                {
                    TranslateTopic(topic);
                }
            }
            catch (Exception ex)
            {
                Hook.Log("Translation loop error: " + ex.ToString());
            }
        }

        private static void TranslateTopic(GameLibrary.HelpTopic topic)
        {
            if (topic == null) return;
            if (translatedTopics.Contains(topic)) return;

            // Translate Title
            if (!string.IsNullOrEmpty(topic.Title))
            {
                topic.Title = Hook.ProcessText(topic.Title);
            }

            // Translate BodyItems
            if (topic.BodyItems != null)
            {
                foreach (var bodyItem in topic.BodyItems)
                {
                    if (bodyItem != null && bodyItem.Type == GameLibrary.HelpBodyItemType.Text && !string.IsNullOrEmpty(bodyItem.Body))
                    {
                        bodyItem.Body = Hook.ProcessText(bodyItem.Body);
                    }
                }
            }

            translatedTopics.Add(topic);

            // Translate subtopics
            if (topic.Topics != null)
            {
                foreach (var subtopic in topic.Topics)
                {
                    TranslateTopic(subtopic);
                }
            }
        }
    }
}
