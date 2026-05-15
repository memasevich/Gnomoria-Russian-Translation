using System;
using System.IO;
using System.Collections.Generic;
using System.Drawing;
using System.Drawing.Text;
using System.Drawing.Drawing2D;
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
                File.WriteAllText("TranslatorHook.log", "Hook v2.8 [Universal Engine] Init\n");
                string fullPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, LogPath);
                
                if (File.Exists(fullPath))
                {
                    string rawJson = File.ReadAllText(fullPath);
                    rawJson = rawJson.Replace("\\\"", "\""); 
                    try {
                        Translations = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, string>>(rawJson) ?? new Dictionary<string, string>();
                        foreach(var k in Translations.Keys) FoundStrings.Add(k);
                        File.AppendAllText("TranslatorHook.log", "Loaded " + Translations.Count + " translations.\n");
                    } catch (Exception ex) {
                        File.AppendAllText("TranslatorHook.log", "JSON Parse Error: " + ex.Message + "\n");
                    }
                }
                
                var harmony = new Harmony("com.lecoo.gnomoriatranslator");
                harmony.PatchAll();
                File.AppendAllText("TranslatorHook.log", "Harmony: 4 Overloads Patched.\n");
            }
            catch (Exception ex) { File.AppendAllText("TranslatorHook.log", "Init Error: " + ex.ToString() + "\n"); }
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

    // --- OVERLOAD 1: String (Simple) ---
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

    // --- OVERLOAD 2: String (Complex) ---
    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public static class Patch_DS2 {
        static bool Prefix(SpriteBatch __instance, string text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth) {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text)) { Hook.FoundStrings.Add(text); Hook.Translations[text] = text; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(text, out string t) && text != t) {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, t);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(text, position), null, color, rotation, origin, scale, effects, layerDepth); return false; }
            }
            return true;
        }
    }

    // --- OVERLOAD 3: StringBuilder (Simple) ---
    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public static class Patch_DS3 {
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

    // --- OVERLOAD 4: StringBuilder (Complex) ---
    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public static class Patch_DS4 {
        static bool Prefix(SpriteBatch __instance, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth) {
            if (text == null || text.Length == 0) return true;
            string s = text.ToString();
            if (!Hook.FoundStrings.Contains(s)) { Hook.FoundStrings.Add(s); Hook.Translations[s] = s; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(s, out string t) && s != t) {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, t);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(s, position), null, color, rotation, origin, scale, effects, layerDepth); return false; }
            }
            return true;
        }
    }
}
