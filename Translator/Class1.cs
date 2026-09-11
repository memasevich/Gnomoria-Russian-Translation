// Gnomoria Russian Translation
// Developer: memasevich
// Release line: v0.6.0

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using System.Text;
using System.Drawing;
using System.Drawing.Text;
using System.Drawing.Drawing2D;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;
using HarmonyLib;
using Newtonsoft.Json;
using System.Text.RegularExpressions;

namespace GnomoriaTranslator
{
    public class Hook
    {
        public static Dictionary<string, string> Translations = new Dictionary<string, string>();
        public static Dictionary<string, Texture2D> TextureCache = new Dictionary<string, Texture2D>();
        
        public static void Log(string msg) {
            try { File.AppendAllText(@"D:\steam\steamapps\common\Gnomoria\TranslatorHook.log", msg + "\n"); } catch { }
        }

        public static void Init()
        {
            try
            {
                Log("\nHook v5.5 [FONT FIX] Init at " + DateTime.Now.ToString());
                string jsonPath = @"D:\steam\steamapps\common\Gnomoria\Gnomoria_en_ru.json";
                if (File.Exists(jsonPath))
                {
                    Translations = JsonConvert.DeserializeObject<Dictionary<string, string>>(File.ReadAllText(jsonPath, new UTF8Encoding(true)));
                    Log("Loaded " + Translations.Count + " entries.");
                }

                var harmony = new Harmony("com.lecoo.gnomoriatranslator.dynamic");
                var methods = typeof(SpriteBatch).GetMethods().Where(m => m.Name == "DrawString").ToList();

                foreach (var m in methods)
                {
                    var parameters = m.GetParameters();
                    if (parameters.Length >= 4) // Минимум Font, Text, Position, Color
                    {
                        if (parameters[1].ParameterType == typeof(string))
                            harmony.Patch(m, new HarmonyMethod(typeof(Hook).GetMethod("PrefixString")));
                        else if (parameters[1].ParameterType == typeof(StringBuilder))
                            harmony.Patch(m, new HarmonyMethod(typeof(Hook).GetMethod("PrefixSB")));
                    }
                }
                HelpPatcher.Patch(harmony);
                DefsPatcher.Patch(harmony);
                ResolutionPatcher.Patch(harmony);

                // Optional chain-load for GnomoriaOptimizer if present
                try
                {
                    string optPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, "GnomoriaOptimizer.dll");
                    if (File.Exists(optPath))
                    {
                        var optAssembly = System.Reflection.Assembly.LoadFrom(optPath);
                        var hookType = optAssembly.GetType("GnomoriaOptimizer.Hook");
                        var initMethod = hookType?.GetMethod("Init", System.Reflection.BindingFlags.Public | System.Reflection.BindingFlags.Static);
                        initMethod?.Invoke(null, null);
                        Log("Chain-loaded GnomoriaOptimizer successfully.");
                    }
                }
                catch (Exception exOpt)
                {
                    Log("Optimizer chain-load warning: " + exOpt.Message);
                }
            }
            catch (Exception ex) { Log("Init Error: " + ex.ToString()); }
        }

        // ПРЕФИКС ДЛЯ СТРОК
        public static bool PrefixString(SpriteBatch __instance, SpriteFont spriteFont, ref string text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            text = ProcessText(text);
            if (ContainsRussian(text))
            {
                DrawCustomText(__instance, text, position, color);
                return false; // Пропускаем оригинальный DrawString
            }
            return true;
        }

        // ПРЕФИКС ДЛЯ StringBuilder
        public static bool PrefixSB(SpriteBatch __instance, SpriteFont spriteFont, StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            if (text == null) return true;
            string original = text.ToString();
            string translated = ProcessText(original);
            
            if (ContainsRussian(translated))
            {
                DrawCustomText(__instance, translated, position, color);
                return false; // Пропускаем
            }
            return true;
        }

        private static bool ContainsRussian(string text)
        {
            return text.Any(c => (c >= 'а' && c <= 'я') || (c >= 'А' && c <= 'Я') || c == 'ё' || c == 'Ё');
        }

        private static void DrawCustomText(SpriteBatch sb, string text, Vector2 pos, Microsoft.Xna.Framework.Color color)
        {
            Texture2D tex;
            if (!TextureCache.TryGetValue(text, out tex))
            {
                tex = CreateTextTexture(sb.GraphicsDevice, text);
                TextureCache[text] = tex;
            }
            if (tex != null)
            {
                sb.Draw(tex, pos, color);
            }
        }

        public static string ProcessText(string text)
        {
            if (string.IsNullOrEmpty(text)) return text;
            string trimmed = text.Trim();
            string res;
            if (Translations.TryGetValue(trimmed, out res)) return res;
            if (TryTranslateDynamic(trimmed, out res)) return res;

            // Префиксы
            if (trimmed.StartsWith("Year ")) return trimmed.Replace("Year ", "Год ");
            if (trimmed.StartsWith("Day ")) return trimmed.Replace("Day ", "День ");
            if (trimmed.StartsWith("Depth: ")) return trimmed.Replace("Depth: ", "Глубина: ");
            if (trimmed.StartsWith("Nourishment Weight: ")) return trimmed.Replace("Nourishment Weight: ", "Важность питания: ");
            if (trimmed.StartsWith("Action Button ")) return trimmed.Replace("Action Button ", "Кн. действия ");
            if (trimmed.StartsWith("Set Bookmark ")) return trimmed.Replace("Set Bookmark ", "Уст. закладку ");
            if (trimmed.StartsWith("Bookmark ")) return trimmed.Replace("Bookmark ", "Закладка ");

            // Перевод профессий гномов (например, "Trixilli Farmer" -> "Trixilli Фермер")
            string[] englishProfs = new string[] { "Miner", "Carpenter", "Stonecutter", "Blacksmith", "Tailor", "Leatherworker", "Woodcutter", "Farmer", "Builder", "Soldier", "Doctor", "Hauler", "Rancher", "Weaver", "Engineer", "Jeweler" };
            string[] russianProfs = new string[] { "Шахтёр", "Плотник", "Камнерез", "Кузнец", "Портной", "Кожевник", "Лесоруб", "Фермер", "Строитель", "Солдат", "Доктор", "Носильщик", "Скотовод", "Ткач", "Инженер", "Ювелир" };
            for (int i = 0; i < englishProfs.Length; i++)
            {
                if (trimmed.EndsWith(" " + englishProfs[i]))
                {
                    return trimmed.Substring(0, trimmed.Length - englishProfs[i].Length) + russianProfs[i];
                }
            }

            int lastSpace = trimmed.LastIndexOf(' ');
            if (lastSpace > 0 && lastSpace < trimmed.Length - 1)
            {
                string suffixWord = trimmed.Substring(lastSpace + 1);
                if (Translations.TryGetValue(suffixWord, out string trSuffix) && trSuffix != suffixWord)
                {
                    return trimmed.Substring(0, lastSpace + 1) + trSuffix;
                }
            }

            // Деревья
            if (trimmed == "birch tree") return "берёза";
            if (trimmed == "pine tree") return "сосна";
            if (trimmed == "apple tree") return "яблоня";
            if (trimmed == "orange tree") return "апельсиновое дерево";
            if (trimmed == "peach tree") return "персиковое дерево";
            if (trimmed == "pear tree") return "грушевое дерево";
            if (trimmed == "cherry tree") return "вишнёвое дерево";
            if (trimmed == "mahogany tree") return "махагони";

            // Полы
            if (trimmed == "dirt floor") return "земляной пол";
            if (trimmed == "stone floor") return "каменный пол";
            if (trimmed == "wood floor") return "деревянный пол";
            if (trimmed == "plank floor") return "дощатый пол";
            if (trimmed == "block floor") return "блочный пол";
            if (trimmed == "straw floor") return "соломенный пол";
            if (trimmed == "clay floor") return "глиняный пол";

            // Стены
            if (trimmed == "dirt wall") return "земляная стена";
            if (trimmed == "stone wall") return "каменная стена";
            if (trimmed == "wood wall") return "деревянная стена";
            if (trimmed == "plank wall") return "дощатая стена";
            if (trimmed == "block wall") return "блочная стена";
            if (trimmed == "straw wall") return "соломенная стена";
            if (trimmed == "clay wall") return "глиняная стена";
            
            // Логируем пропущенное (исключая шум таймера скорости)
            if (trimmed.Any(char.IsLetter) && !ContainsRussian(trimmed) && !IsNoise(trimmed))
            {
                try { File.AppendAllText(@"D:\steam\steamapps\common\Gnomoria\TOTAL_LOG.txt", trimmed + "\n"); } catch { }
            }

            return text;
        }

        private static bool TryTranslateDynamic(string text, out string result)
        {
            result = null;

            if (TryTranslatePrefix(text, "Food:", "Еда:", out result)) return true;
            if (TryTranslatePrefix(text, "Drink:", "Питьё:", out result)) return true;
            if (TryTranslatePrefix(text, "Drink...", "Питьё...", out result)) return true;
            if (TryTranslatePrefix(text, "Sunrise:", "Восход:", out result)) return true;
            if (TryTranslatePrefix(text, "Sunset:", "Закат:", out result)) return true;
            if (TryTranslatePrefix(text, "Worth:", "Ценность:", out result)) return true;
            if (TryTranslatePrefix(text, "Squads:", "Отряды:", out result)) return true;
            if (TryTranslatePrefix(text, "Soldiers:", "Солдаты:", out result)) return true;
            if (TryTranslatePrefix(text, "Assigned:", "Назначено:", out result)) return true;
            if (TryTranslatePrefix(text, "Population:", "Население:", out result)) return true;
            if (TryTranslatePrefix(text, "Deceased:", "Погибшие:", out result)) return true;
            if (TryTranslatePrefix(text, "Injured:", "Раненые:", out result)) return true;
            if (TryTranslatePrefix(text, "Idle:", "Без дела:", out result)) return true;
            if (TryTranslatePrefix(text, "Required Carpentry:", "Требуется плотницкое дело:", out result)) return true;
            if (TryTranslatePrefix(text, "Required Masonry:", "Требуется каменное дело:", out result)) return true;
            if (TryTranslatePrefix(text, "Required Construction:", "Требуется строительство:", out result)) return true;
            if (TryTranslatePrefix(text, "Efficiency:", "Эффективность:", out result)) return true;
            if (TryTranslatePrefix(text, "Available Space:", "Свободное место:", out result)) return true;
            if (TryTranslatePrefix(text, "Crops Ready:", "Готово к сбору:", out result)) return true;
            if (TryTranslatePrefix(text, "Seeds Planted:", "Посажено семян:", out result)) return true;
            if (TryTranslatePrefix(text, "Tilled Plots:", "Вспахано участков:", out result)) return true;
            if (TryTranslatePrefix(text, "Planted:", "Посажено:", out result)) return true;
            if (TryTranslatePrefix(text, "Pastured:", "На выпасе:", out result)) return true;
            if (TryTranslatePrefix(text, "Males:", "Самцы:", out result)) return true;
            if (TryTranslatePrefix(text, "Females:", "Самки:", out result)) return true;
            if (TryTranslatePrefix(text, "Trees:", "Деревья:", out result)) return true;
            if (TryTranslatePrefix(text, "Fruit:", "Плоды:", out result)) return true;
            if (TryTranslatePrefix(text, "Can be clipped:", "Можно стричь:", out result)) return true;
            if (TryTranslatePrefix(text, "No Room:", "Нет места:", out result)) return true;
            if (TryTranslatePrefix(text, "Last played:", "Последняя игра:", out result)) return true;
            if (TryTranslatePrefix(text, "Total (", "Всего (", out result)) return true;
            if (TryTranslatePrefix(text, "Dormitories (", "Общие спальни (", out result)) return true;
            if (TryTranslatePrefix(text, "Personal Quarters (", "Личные комнаты (", out result)) return true;
            if (TryTranslatePrefix(text, "Hospitals (", "Больницы (", out result)) return true;
            if (TryTranslatePrefix(text, "Dining Rooms (", "Столовые (", out result)) return true;
            if (TryTranslatePrefix(text, "any wood door (", "любая деревянная дверь (", out result)) return true;
            if (TryTranslatePrefix(text, "any bed (", "любая кровать (", out result)) return true;
            if (TryTranslatePrefix(text, "wheat straw pile (", "куча пшеничной соломы (", out result)) return true;
            if (TryTranslatePrefix(text, "any log (", "любое бревно (", out result)) return true;
            if (TryTranslatePrefix(text, "any plank (", "любая доска (", out result)) return true;
            if (TryTranslatePrefix(text, "cotton bag (strawberry seed) (", "хлопковый мешок (семена клубники) (", out result)) return true;
            if (TryTranslatePrefix(text, "cotton bag (wheat seed) (", "хлопковый мешок (семена пшеницы) (", out result)) return true;
            if (TryTranslatePrefix(text, "pine crate (", "сосновый ящик (", out result)) return true;
            if (TryTranslatePrefix(text, "any raw stone (", "любой необработанный камень (", out result)) return true;
            if (TryTranslatePrefix(text, "any crate (", "любой ящик (", out result)) return true;
            if (TryTranslatePrefix(text, "dirt pile (", "куча земли (", out result)) return true;

            if (TryTranslatePrefix(text, "Distance:", "Расстояние:", out result))
            {
                result = result.Replace(" days ", " дн. ").Replace(" hours", " ч.");
                return true;
            }

            // Задачи вида "Task: Build Sawmill", "Task: Craft Item"
            if (text.StartsWith("Task: ", StringComparison.OrdinalIgnoreCase))
            {
                string subAction = text.Substring(6).Trim();
                result = "Задача: " + ProcessText(subAction);
                return true;
            }

            // Навыки с уровнем в скобках вида "(26) Mining", "(4) Pottery"
            if (TryTranslateNumberedSkill(text, out result)) return true;

            // Календарные даты вида "2nd day of Spring, Year 1", "2nd day of Spring"
            if (TryTranslateDate(text, out result)) return true;

            // Навыки гномов, характеристики и числовые префиксы с двоеточием вида "Mining: 24", "Pastured Animals: 0/20"
            if (TryTranslateColonValue(text, out result)) return true;

            // Профессии с двоеточием вида "miner:", "farmer:"
            if (TryTranslateSingleColonWord(text, out result)) return true;

            // Количество с предметом вида "1x raw stone (19)", "16x raw stone", "479x clump"
            if (TryTranslateQuantity(text, out result)) return true;

            // Предмет с количеством на складе вида "any barrel (2)", "alpaca (0)", "yak (2)"
            if (TryTranslateItemWithCount(text, out result)) return true;

            // Игровые события (смерти, появление врагов, кочевники, сезоны, кровь, останки)
            if (TryTranslateGameEvents(text, out result)) return true;

            // События сна и усталости
            if (TryTranslateSleepEvent(text, out result)) return true;

            // Зависимости и верстак
            if (TryTranslateWorkbenchCraft(text, out result)) return true;

            return false;
        }

        private static readonly Regex DateRegex = new Regex(@"^(\d+)(?:st|nd|rd|th)\s+day\s+of\s+(Spring|Summer|Autumn|Winter)(?:,\s*Year\s*(\d+))?$", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex NumberedSkillRegex = new Regex(@"^\((\d+)\)\s+(.+)$", RegexOptions.Compiled);
        private static readonly Regex QuantityRegex = new Regex(@"^(\d+x)\s+(.+?)(?:\s*(\(\d+\)))?$", RegexOptions.Compiled);
        private static readonly Regex AnyItemWithCountRegex = new Regex(@"^any\s+(.+?)\s*\((\d+)\)$", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex ItemWithCountRegex = new Regex(@"^([A-Za-z][A-Za-z0-9\s-]*?)\s*\((\d+)\)$", RegexOptions.Compiled);
        private static readonly Regex GnomadsRegex = new Regex(@"^(\d+)\s+gnomads have arrived\.$", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex WaterRegex = new Regex(@"^(\d+)%\s+water$", RegexOptions.IgnoreCase | RegexOptions.Compiled);
        private static readonly Regex NoiseRegex = new Regex(@"^\(\d+(\.\d+)?x\)\s+\d{1,2}:\d{2}$", RegexOptions.Compiled);
        private static readonly Regex DimensionNoiseRegex = new Regex(@"^\d+\s*x\s*\d+$", RegexOptions.Compiled);
        private static readonly Regex SpeedNoiseRegex = new Regex(@"^\d+x$", RegexOptions.Compiled);
        private static readonly Regex HotkeyNoiseRegex = new Regex(@"^(?:(?:Left|Right)?(?:Control|Alt|Shift)\s*\+\s*.*|F\d{1,2}|Space|Enter|Escape|Tab|[A-Z])$", RegexOptions.Compiled);

        private static bool TryTranslateNumberedSkill(string text, out string result)
        {
            result = null;
            var match = NumberedSkillRegex.Match(text);
            if (!match.Success) return false;
            string num = match.Groups[1].Value;
            string skill = match.Groups[2].Value.Trim();
            string trSkill = ProcessText(skill);
            if (trSkill != skill || ContainsRussian(trSkill))
            {
                result = "(" + num + ") " + trSkill;
                return true;
            }
            return false;
        }

        private static bool TryTranslateQuantity(string text, out string result)
        {
            result = null;
            var match = QuantityRegex.Match(text);
            if (!match.Success) return false;

            string count = match.Groups[1].Value;
            string item = match.Groups[2].Value.Trim();
            string inStock = match.Groups[3].Success ? match.Groups[3].Value : null;

            string trItem = ProcessText(item);
            if (trItem != item || ContainsRussian(trItem))
            {
                result = count + " " + trItem + (string.IsNullOrEmpty(inStock) ? "" : " " + inStock);
                return true;
            }
            return false;
        }

        private static bool TryTranslateItemWithCount(string text, out string result)
        {
            result = null;
            var anyMatch = AnyItemWithCountRegex.Match(text);
            if (anyMatch.Success)
            {
                string item = anyMatch.Groups[1].Value.Trim();
                string count = anyMatch.Groups[2].Value;
                string fullAny = "any " + item;
                if (Translations.TryGetValue(fullAny, out string trAny))
                {
                    result = trAny + " (" + count + ")";
                    return true;
                }
                string trItem = ProcessText(item);
                result = "любой: " + trItem + " (" + count + ")";
                return true;
            }

            var match = ItemWithCountRegex.Match(text);
            if (match.Success)
            {
                string item = match.Groups[1].Value.Trim();
                string count = match.Groups[2].Value;
                string trItem = ProcessText(item);
                if (trItem != item || ContainsRussian(trItem))
                {
                    result = trItem + " (" + count + ")";
                    return true;
                }
            }
            return false;
        }

        private static bool TryTranslateSingleColonWord(string text, out string result)
        {
            result = null;
            if (text.EndsWith(":") && !text.Contains(" "))
            {
                string baseWord = text.Substring(0, text.Length - 1);
                if (Translations.TryGetValue(baseWord, out string trWord))
                {
                    result = trWord + ":";
                    return true;
                }
            }
            return false;
        }

        private static bool TryTranslateDate(string text, out string result)
        {
            result = null;
            var match = DateRegex.Match(text);
            if (!match.Success) return false;

            string day = match.Groups[1].Value;
            string seasonEng = match.Groups[2].Value.ToLowerInvariant();
            string seasonRu;
            switch (seasonEng)
            {
                case "spring": seasonRu = "весны"; break;
                case "summer": seasonRu = "лета"; break;
                case "autumn": seasonRu = "осени"; break;
                case "winter": seasonRu = "зимы"; break;
                default: seasonRu = seasonEng; break;
            }

            if (match.Groups[3].Success)
            {
                result = day + "-й день " + seasonRu + ", Год " + match.Groups[3].Value;
            }
            else
            {
                result = day + "-й день " + seasonRu;
            }
            return true;
        }

        private static bool TryTranslateColonValue(string text, out string result)
        {
            result = null;
            int colonIdx = text.IndexOf(':');
            if (colonIdx > 0 && colonIdx < text.Length - 1)
            {
                string prefix = text.Substring(0, colonIdx + 1);
                string suffix = text.Substring(colonIdx + 1).Trim();

                if (Translations.TryGetValue(prefix, out string trPrefix))
                {
                    if (Translations.TryGetValue(suffix, out string trSuffix))
                    {
                        result = trPrefix + " " + trSuffix;
                        return true;
                    }

                    if (TryTranslateDate(suffix, out string trDate))
                    {
                        result = trPrefix + " " + trDate;
                        return true;
                    }

                    if (suffix.Length > 0 && suffix.All(c => char.IsDigit(c) || c == '/' || c == ' ' || c == '%'))
                    {
                        result = trPrefix + " " + suffix;
                        return true;
                    }

                    string trOther = ProcessText(suffix);
                    if (trOther != suffix || ContainsRussian(trOther))
                    {
                        result = trPrefix + " " + trOther;
                        return true;
                    }
                }
            }
            return false;
        }

        private static bool TryTranslateGameEvents(string text, out string result)
        {
            result = null;

            if (text.EndsWith(" has died.", StringComparison.OrdinalIgnoreCase))
            {
                string name = text.Substring(0, text.Length - 10).Trim();
                if (name.Equals("The goblin", StringComparison.OrdinalIgnoreCase))
                {
                    result = "Гоблин погиб.";
                }
                else
                {
                    result = name + " погибает.";
                }
                return true;
            }

            if (text.EndsWith(" has bled to death.", StringComparison.OrdinalIgnoreCase))
            {
                string name = text.Substring(0, text.Length - 20).Trim();
                result = name + " истекает кровью до смерти.";
                return true;
            }

            if (text.StartsWith("A ", StringComparison.OrdinalIgnoreCase) && text.EndsWith(" has been spotted.", StringComparison.OrdinalIgnoreCase))
            {
                string creature = text.Substring(2, text.Length - 2 - 18).Trim();
                if (Translations.TryGetValue(creature, out string trCreature))
                {
                    result = "Замечен: " + trCreature + ".";
                    return true;
                }
            }

            if (text.StartsWith("a goblin is now known as ", StringComparison.OrdinalIgnoreCase))
            {
                result = "Гоблин теперь известен как " + text.Substring(25);
                return true;
            }

            var gnomadMatch = GnomadsRegex.Match(text);
            if (gnomadMatch.Success)
            {
                result = gnomadMatch.Groups[1].Value + " прибыло гномов-кочевников.";
                return true;
            }

            if (text.Equals("It is now summer.", StringComparison.OrdinalIgnoreCase)) { result = "Наступило лето."; return true; }
            if (text.Equals("It is now spring.", StringComparison.OrdinalIgnoreCase)) { result = "Наступила весна."; return true; }
            if (text.Equals("It is now autumn.", StringComparison.OrdinalIgnoreCase)) { result = "Наступила осень."; return true; }
            if (text.Equals("It is now winter.", StringComparison.OrdinalIgnoreCase)) { result = "Наступила зима."; return true; }

            if (text.EndsWith("'s corpse", StringComparison.OrdinalIgnoreCase))
            {
                result = "Труп: " + text.Substring(0, text.Length - 9);
                return true;
            }
            if (text.EndsWith("'s blood", StringComparison.OrdinalIgnoreCase))
            {
                result = "Кровь: " + text.Substring(0, text.Length - 8);
                return true;
            }

            var waterMatch = WaterRegex.Match(text);
            if (waterMatch.Success)
            {
                result = waterMatch.Groups[1].Value + "% воды";
                return true;
            }

            if (text.EndsWith(" is in good health", StringComparison.OrdinalIgnoreCase))
            {
                result = text.Substring(0, text.Length - 18) + " в добром здравии";
                return true;
            }

            return false;
        }

        private static bool TryTranslateSleepEvent(string text, out string result)
        {
            result = null;
            const string sleepSuffix = " falls asleep on the floor.";
            if (text.EndsWith(sleepSuffix, StringComparison.OrdinalIgnoreCase))
            {
                string name = text.Substring(0, text.Length - sleepSuffix.Length);
                result = name + " засыпает на полу.";
                return true;
            }
            const string exhaustSuffix = " passes out from exhaustion.";
            if (text.EndsWith(exhaustSuffix, StringComparison.OrdinalIgnoreCase))
            {
                string name = text.Substring(0, text.Length - exhaustSuffix.Length);
                result = name + " падает от истощения.";
                return true;
            }
            return false;
        }

        private static bool TryTranslateWorkbenchCraft(string text, out string result)
        {
            result = null;

            // "Crude Workbench (Efficiency: 70%)"
            const string effTag = " (Efficiency: ";
            int effIdx = text.IndexOf(effTag, StringComparison.OrdinalIgnoreCase);
            if (effIdx > 0 && text.EndsWith(")"))
            {
                string wsName = text.Substring(0, effIdx);
                string effPart = text.Substring(effIdx + effTag.Length).TrimEnd(')');
                result = ProcessText(wsName) + " (Эффективность: " + effPart + ")";
                return true;
            }

            // "plank (for workbench)"
            const string forTag = " (for ";
            int forIdx = text.IndexOf(forTag, StringComparison.OrdinalIgnoreCase);
            if (forIdx > 0 && text.EndsWith(")"))
            {
                string itemPart = text.Substring(0, forIdx);
                string forPart = text.Substring(forIdx + forTag.Length).TrimEnd(')');
                result = ProcessText(itemPart) + " (для: " + ProcessText(forPart) + ")";
                return true;
            }

            // "chair (needs plank)"
            const string needsTag = " (needs ";
            int needsIdx = text.IndexOf(needsTag, StringComparison.OrdinalIgnoreCase);
            if (needsIdx > 0 && text.EndsWith(")"))
            {
                string itemPart = text.Substring(0, needsIdx);
                string needsPart = text.Substring(needsIdx + needsTag.Length).TrimEnd(')');
                result = ProcessText(itemPart) + " (требуется: " + ProcessText(needsPart) + ")";
                return true;
            }

            // "For workbench at"
            if (text.StartsWith("For ", StringComparison.OrdinalIgnoreCase) && text.EndsWith(" at", StringComparison.OrdinalIgnoreCase))
            {
                string target = text.Substring(4, text.Length - 7).Trim();
                result = "Для: " + ProcessText(target) + " в";
                return true;
            }

            // "Craft plank"
            if (text.StartsWith("Craft ", StringComparison.OrdinalIgnoreCase))
            {
                string item = text.Substring(6).Trim();
                result = "Создать: " + ProcessText(item);
                return true;
            }

            // "Build Sawmill"
            if (text.StartsWith("Build ", StringComparison.OrdinalIgnoreCase) && !text.StartsWith("Build a ", StringComparison.OrdinalIgnoreCase))
            {
                string ws = text.Substring(6).Trim();
                if (Translations.TryGetValue(ws, out string wsRu))
                {
                    result = "Построить: " + wsRu;
                    return true;
                }
            }

            // "workbench (for build jo..."
            if (text.Contains("(for build jo"))
            {
                int idx = text.IndexOf("(for build jo");
                string itm = text.Substring(0, idx).Trim();
                result = ProcessText(itm) + " (для стройки...)";
                return true;
            }
            if (text.Contains("(for bed) (ne"))
            {
                int idx = text.IndexOf("(for bed) (ne");
                string itm = text.Substring(0, idx).Trim();
                result = ProcessText(itm) + " (для кровати) (нуж...)";
                return true;
            }
            if (text.StartsWith("Needs plank at", StringComparison.OrdinalIgnoreCase))
            {
                result = "Требуется доска в";
                return true;
            }

            return false;
        }

        private static bool IsNoise(string text)
        {
            if (NoiseRegex.IsMatch(text)) return true;
            if (DimensionNoiseRegex.IsMatch(text)) return true;
            if (SpeedNoiseRegex.IsMatch(text)) return true;
            if (HotkeyNoiseRegex.IsMatch(text)) return true;
            if (text.Equals("v1.0", StringComparison.OrdinalIgnoreCase)) return true;
            return false;
        }

        private static bool TryTranslatePrefix(string text, string englishPrefix, string russianPrefix, out string result)
        {
            if (text.StartsWith(englishPrefix, StringComparison.OrdinalIgnoreCase))
            {
                result = russianPrefix + text.Substring(englishPrefix.Length);
                return true;
            }

            result = null;
            return false;
        }

        private static Texture2D CreateTextTexture(GraphicsDevice device, string text)
        {
            try
            {
                // Настройки шрифта (Возвращаем оригинальный Arial 12px Regular, Unit: Pixel)
                using (var font = new System.Drawing.Font("Arial", 12f, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Pixel))
                {
                    // Измеряем текст
                    using (var tempBmp = new Bitmap(1, 1))
                    using (var g = System.Drawing.Graphics.FromImage(tempBmp))
                    {
                        var size = g.MeasureString(text, font);
                        int w = (int)Math.Ceiling(size.Width + 4);
                        int h = (int)Math.Ceiling(size.Height + 2);
                        if (w <= 0 || h <= 0) return null;

                        using (var bmp = new Bitmap(w, h))
                        using (var g2 = System.Drawing.Graphics.FromImage(bmp))
                        {
                            g2.TextRenderingHint = TextRenderingHint.AntiAliasGridFit; // Оригинальное сглаживание
                            g2.Clear(System.Drawing.Color.Transparent);
                            g2.DrawString(text, font, System.Drawing.Brushes.White, 0, 0);

                            // Конвертируем в XNA Texture2D
                            var data = new Microsoft.Xna.Framework.Color[w * h];
                            for (int y = 0; y < h; y++)
                            {
                                for (int x = 0; x < w; x++)
                                {
                                    var c = bmp.GetPixel(x, y);
                                    data[y * w + x] = new Microsoft.Xna.Framework.Color(c.R, c.G, c.B, c.A);
                                }
                            }
                            var tex = new Texture2D(device, w, h);
                            tex.SetData(data);
                            return tex;
                        }
                    }
                }
            }
            catch { return null; }
        }
    }
}
