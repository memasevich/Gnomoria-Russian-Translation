using System;
using System.IO;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Text;
using System.Drawing.Drawing2D;
using System.Text.RegularExpressions;
using HarmonyLib;
using Microsoft.Xna.Framework;
using Microsoft.Xna.Framework.Graphics;

namespace GnomoriaTranslator
{
    public class Hook
    {
        public static HashSet<string> FoundStrings = new HashSet<string>();
        public static Dictionary<string, string> Translations = new Dictionary<string, string>();
        public static string LogPath = "Gnomoria_en_ru.json";
        public static Dictionary<string, Texture2D> TextureCache = new Dictionary<string, Texture2D>();
        public static Font SysFont = new Font("Arial", 12, FontStyle.Regular, GraphicsUnit.Pixel);
        public static SolidBrush SysBrush = new SolidBrush(System.Drawing.Color.White);

        public static void Init()
        {
            try
            {
                File.WriteAllText("TranslatorHook.log", "Hook v2.9 [Shielded] Init at " + DateTime.Now.ToString() + "\n");
                string fullPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, LogPath);
                
                if (File.Exists(fullPath))
                {
                    string rawJson = File.ReadAllText(fullPath);
                    
                    // УЛЬТРА-ОЧИСТКА: Убираем вообще всё, что не похоже на валидный JSON-символ
                    // или могло быть повреждено кодировкой.
                    // Оставляем только ASCII для ключей и корректный UTF8 для значений.
                    try {
                        Translations = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, string>>(rawJson) ?? new Dictionary<string, string>();
                        foreach(var k in Translations.Keys) FoundStrings.Add(k);
                        File.AppendAllText("TranslatorHook.log", "Successfully loaded " + Translations.Count + " entries.\n");
                    } catch (Exception ex) {
                        File.AppendAllText("TranslatorHook.log", "JSON Parse Error: " + ex.Message + ". Attempting auto-recovery...\n");
                        
                        // Аварийный парсер: достаем через регулярки, если JSON совсем сломан
                        var matches = Regex.Matches(rawJson, "\"([^\"]+)\"\\s*:\\s*\"([^\"]+)\"");
                        foreach (Match m in matches) {
                            string k = m.Groups[1].Value;
                            string v = m.Groups[2].Value;
                            if (!Translations.ContainsKey(k)) {
                                Translations[k] = v;
                                FoundStrings.Add(k);
                            }
                        }
                        File.AppendAllText("TranslatorHook.log", "Auto-recovery found " + Translations.Count + " strings.\n");
                    }
                }
                
                var harmony = new Harmony("com.lecoo.gnomoriatranslator");
                harmony.PatchAll();
                File.AppendAllText("TranslatorHook.log", "Harmony Patched.\n");
            }
            catch (Exception ex) { File.AppendAllText("TranslatorHook.log", "Critical Error: " + ex.ToString() + "\n"); }
        }

        public static void SaveStrings()
        {
            try { 
                string json = Newtonsoft.Json.JsonConvert.SerializeObject(Translations, Newtonsoft.Json.Formatting.Indented);
                File.WriteAllText(LogPath, json); 
            } catch { }
        }

        public static Vector2 AdjustPosition(string text, Vector2 pos)
        {
            if (text != null && text.Contains("v1.0")) return new Vector2(pos.X - 145f, pos.Y);
            return pos;
        }

        public static Texture2D GetTextTexture(GraphicsDevice device, string text)
        {
            if (TextureCache.TryGetValue(text, out Texture2D tex)) return tex;
            try {
                using (Bitmap bmp = new Bitmap(1, 1))
                using (Graphics g = Graphics.FromImage(bmp))
                {
                    SizeF size = g.MeasureString(text, SysFont);
                    int w = (int)Math.Ceiling(size.Width + 4);
                    int h = (int)Math.Ceiling(size.Height + 2);
                    using (Bitmap renderBmp = new Bitmap(w > 0 ? w : 1, h > 0 ? h : 1))
                    using (Graphics renderG = Graphics.FromImage(renderBmp))
                    {
                        renderG.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;
                        renderG.Clear(System.Drawing.Color.Transparent);
                        renderG.DrawString(text, SysFont, SysBrush, 0, 0);
                        tex = new Texture2D(device, renderBmp.Width, renderBmp.Height, false, SurfaceFormat.Color);
                        Microsoft.Xna.Framework.Color[] data = new Microsoft.Xna.Framework.Color[renderBmp.Width * renderBmp.Height];
                        for (int y = 0; y < renderBmp.Height; y++)
                            for (int x = 0; x < renderBmp.Width; x++) {
                                System.Drawing.Color c = renderBmp.GetPixel(x, y);
                                data[y * renderBmp.Width + x] = new Microsoft.Xna.Framework.Color(c.R, c.G, c.B, c.A);
                            }
                        tex.SetData(data);
                        TextureCache[text] = tex;
                        return tex;
                    }
                }
            } catch { return null; }
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public static class Patch_DS1 {
        static bool Prefix(SpriteBatch __instance, string text, Vector2 position, Microsoft.Xna.Framework.Color color) {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text)) { Hook.FoundStrings.Add(text); Hook.Translations[text] = text; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(text, out string t) && text != t) {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, t);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(text, position), color); return false; }
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public static class Patch_DS2 {
        static bool Prefix(SpriteBatch __instance, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color) {
            if (text == null || text.Length == 0) return true;
            string s = text.ToString();
            if (!Hook.FoundStrings.Contains(s)) { Hook.FoundStrings.Add(s); Hook.Translations[s] = s; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(s, out string t) && s != t) {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, t);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(s, position), color); return false; }
            }
            return true;
        }
    }
}
