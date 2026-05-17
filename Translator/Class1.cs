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
                ResolutionPatcher.Patch(harmony);
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

            // Префиксы
            if (trimmed.StartsWith("Year ")) return trimmed.Replace("Year ", "Год ");
            if (trimmed.StartsWith("Day ")) return trimmed.Replace("Day ", "День ");
            if (trimmed.StartsWith("Depth: ")) return trimmed.Replace("Depth: ", "Глубина: ");
            if (trimmed.StartsWith("Nourishment Weight: ")) return trimmed.Replace("Nourishment Weight: ", "Важность питания: ");
            if (trimmed.StartsWith("Action Button ")) return trimmed.Replace("Action Button ", "Кн. действия ");
            if (trimmed.StartsWith("Set Bookmark ")) return trimmed.Replace("Set Bookmark ", "Уст. закладку ");
            if (trimmed.StartsWith("Bookmark ")) return trimmed.Replace("Bookmark ", "Закладка ");

            // Перевод профессий гномов (например, "Trixilli Farmer" -> "Trixilli Фермер")
            string[] englishProfs = new string[] { "Miner", "Carpenter", "Stonecutter", "Blacksmith", "Tailor", "Leatherworker", "Woodcutter", "Farmer", "Builder", "Soldier", "Doctor", "Hauler", "Rancher", "Weaver" };
            string[] russianProfs = new string[] { "Шахтёр", "Плотник", "Камнерез", "Кузнец", "Портной", "Кожевник", "Лесоруб", "Фермер", "Строитель", "Солдат", "Доктор", "Носильщик", "Скотовод", "Ткач" };
            for (int i = 0; i < englishProfs.Length; i++)
            {
                if (trimmed.EndsWith(" " + englishProfs[i]))
                {
                    return trimmed.Substring(0, trimmed.Length - englishProfs[i].Length) + russianProfs[i];
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
            
            // Логируем пропущенное
            if (trimmed.Any(char.IsLetter) && !ContainsRussian(trimmed))
            {
                try { File.AppendAllText(@"D:\steam\steamapps\common\Gnomoria\TOTAL_LOG.txt", trimmed + "\n"); } catch { }
            }

            return text;
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
