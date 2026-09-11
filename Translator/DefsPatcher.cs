using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection;
using HarmonyLib;
using GameLibrary;

namespace GnomoriaTranslator
{
    public static class DefsPatcher
    {
        public static void Patch(Harmony harmony)
        {
            try
            {
                Type gameDefsType = null;
                foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
                {
                    gameDefsType = asm.GetType("Game.GameDefs");
                    if (gameDefsType != null) break;
                }

                if (gameDefsType != null)
                {
                    Hook.Log("Found GameDefs type! Patching ReadDefs...");
                    var method = gameDefsType.GetMethod("ReadDefs", BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance);
                    if (method != null)
                    {
                        harmony.Patch(method, postfix: new HarmonyMethod(typeof(DefsPatcher), nameof(Postfix)));
                        Hook.Log("Successfully patched GameDefs.ReadDefs!");
                    }
                    else
                    {
                        Hook.Log("ERROR: ReadDefs method not found in GameDefs!");
                    }
                }
                else
                {
                    Hook.Log("ERROR: GameDefs type not found!");
                }
            }
            catch (Exception ex)
            {
                Hook.Log("DefsPatcher Patch Error: " + ex.ToString());
            }
        }

        public static void Postfix(object __instance)
        {
            if (__instance == null) return;
            try
            {
                Hook.Log("DefsPatcher.Postfix: translating GameDefs data tables...");
                Type gameDefsType = __instance.GetType();

                // 1. ItemDefs
                try
                {
                    var itemDefsProp = gameDefsType.GetProperty("ItemDefs");
                    if (itemDefsProp != null)
                    {
                        var itemDefs = itemDefsProp.GetValue(__instance, null) as IDictionary;
                        if (itemDefs != null)
                        {
                            int count = 0;
                            foreach (DictionaryEntry entry in itemDefs)
                            {
                                var item = entry.Value as ItemDef;
                                if (item != null)
                                {
                                    if (!string.IsNullOrEmpty(item.Name)) item.Name = Hook.ProcessText(item.Name);
                                    if (!string.IsNullOrEmpty(item.Description)) item.Description = Hook.ProcessText(item.Description);
                                    if (!string.IsNullOrEmpty(item.ObtainDescription)) item.ObtainDescription = Hook.ProcessText(item.ObtainDescription);
                                    if (!string.IsNullOrEmpty(item.GroupName)) item.GroupName = Hook.ProcessText(item.GroupName);
                                    count++;
                                }
                            }
                            Hook.Log("DefsPatcher: translated " + count + " ItemDefs.");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Hook.Log("DefsPatcher ItemDefs error: " + ex.Message);
                }

                // 2. WorkshopDefs
                try
                {
                    var wsDefsProp = gameDefsType.GetProperty("WorkshopDefs");
                    if (wsDefsProp != null)
                    {
                        var wsDefs = wsDefsProp.GetValue(__instance, null) as IDictionary;
                        if (wsDefs != null)
                        {
                            int count = 0;
                            foreach (DictionaryEntry entry in wsDefs)
                            {
                                var ws = entry.Value as WorkshopDef;
                                if (ws != null)
                                {
                                    if (!string.IsNullOrEmpty(ws.Name)) ws.Name = Hook.ProcessText(ws.Name);
                                    if (!string.IsNullOrEmpty(ws.Description)) ws.Description = Hook.ProcessText(ws.Description);
                                    count++;
                                }
                            }
                            Hook.Log("DefsPatcher: translated " + count + " WorkshopDefs.");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Hook.Log("DefsPatcher WorkshopDefs error: " + ex.Message);
                }

                // 3. ConstructionDefs
                try
                {
                    int cCount = 0;
                    foreach (var field in gameDefsType.GetFields(BindingFlags.Public | BindingFlags.NonPublic | BindingFlags.Instance))
                    {
                        if (typeof(IDictionary).IsAssignableFrom(field.FieldType))
                        {
                            var dict = field.GetValue(__instance) as IDictionary;
                            if (dict != null && dict.Count > 0)
                            {
                                foreach (DictionaryEntry entry in dict)
                                {
                                    var cDef = entry.Value as ConstructionDef;
                                    if (cDef != null)
                                    {
                                        if (!string.IsNullOrEmpty(cDef.Name)) cDef.Name = Hook.ProcessText(cDef.Name);
                                        if (!string.IsNullOrEmpty(cDef.Description)) cDef.Description = Hook.ProcessText(cDef.Description);
                                        if (!string.IsNullOrEmpty(cDef.ToolTip)) cDef.ToolTip = Hook.ProcessText(cDef.ToolTip);
                                        if (!string.IsNullOrEmpty(cDef.GroupName)) cDef.GroupName = Hook.ProcessText(cDef.GroupName);
                                        cCount++;
                                    }
                                }
                            }
                        }
                    }
                    if (cCount > 0)
                    {
                        Hook.Log("DefsPatcher: translated " + cCount + " ConstructionDefs.");
                    }
                }
                catch (Exception ex)
                {
                    Hook.Log("DefsPatcher ConstructionDefs error: " + ex.Message);
                }

                // 4. SkillDefs
                try
                {
                    var skillDefsProp = gameDefsType.GetProperty("SkillDefs");
                    if (skillDefsProp != null)
                    {
                        var skillDefs = skillDefsProp.GetValue(__instance, null) as IDictionary;
                        if (skillDefs != null)
                        {
                            int count = 0;
                            foreach (DictionaryEntry entry in skillDefs)
                            {
                                var skill = entry.Value as SkillDef;
                                if (skill != null)
                                {
                                    if (!string.IsNullOrEmpty(skill.Name)) skill.Name = Hook.ProcessText(skill.Name);
                                    if (!string.IsNullOrEmpty(skill.Title)) skill.Title = Hook.ProcessText(skill.Title);
                                    count++;
                                }
                            }
                            Hook.Log("DefsPatcher: translated " + count + " SkillDefs.");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Hook.Log("DefsPatcher SkillDefs error: " + ex.Message);
                }

                // 5. RaceDefs
                try
                {
                    var raceDefsProp = gameDefsType.GetProperty("RaceDefs");
                    if (raceDefsProp != null)
                    {
                        var raceDefs = raceDefsProp.GetValue(__instance, null) as IDictionary;
                        if (raceDefs != null)
                        {
                            int count = 0;
                            foreach (DictionaryEntry entry in raceDefs)
                            {
                                var race = entry.Value as RaceDef;
                                if (race != null)
                                {
                                    if (!string.IsNullOrEmpty(race.Name)) race.Name = Hook.ProcessText(race.Name);
                                    count++;
                                }
                            }
                            Hook.Log("DefsPatcher: translated " + count + " RaceDefs.");
                        }
                    }
                }
                catch (Exception ex)
                {
                    Hook.Log("DefsPatcher RaceDefs error: " + ex.Message);
                }

                Hook.Log("DefsPatcher.Postfix finished.");
            }
            catch (Exception ex)
            {
                Hook.Log("DefsPatcher.Postfix Fatal Error: " + ex.ToString());
            }
        }
    }
}