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
                File.WriteAllText("TranslatorHook.log", "Hook v2.6 [StringBuilder Enabled] started\n");
                string fullPath = Path.Combine(AppDomain.CurrentDomain.BaseDirectory, LogPath);
                if (File.Exists(fullPath))
                {
                    string json = File.ReadAllText(fullPath);
                    Translations = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, string>>(json) ?? new Dictionary<string, string>();
                    foreach(var k in Translations.Keys) FoundStrings.Add(k);
                    File.AppendAllText("TranslatorHook.log", "Loaded " + Translations.Count + " strings.\n");
                }
                var harmony = new Harmony("com.lecoo.gnomoriatranslator");
                harmony.PatchAll();
            }
            catch (Exception ex) { File.AppendAllText("TranslatorHook.log", "Init Error: " + ex.Message + "\n"); }
        }

        public static void SaveStrings()
        {
            try { File.WriteAllText(LogPath, Newtonsoft.Json.JsonConvert.SerializeObject(Translations, Newtonsoft.Json.Formatting.Indented)); }
            catch { }
        }

        public static Vector2 AdjustPosition(string originalText, Vector2 pos)
        {
            if (originalText != null && originalText.Contains("v1.0")) return new Vector2(pos.X - 145f, pos.Y);
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
                    int width = (int)Math.Ceiling(size.Width + 4);
                    int height = (int)Math.Ceiling(size.Height + 2);
                    using (Bitmap renderBmp = new Bitmap(width > 0 ? width : 1, height > 0 ? height : 1))
                    using (Graphics renderG = Graphics.FromImage(renderBmp))
                    {
                        renderG.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;
                        renderG.Clear(System.Drawing.Color.Transparent);
                        renderG.DrawString(text, SysFont, SysBrush, 0, 0);
                        tex = new Texture2D(device, renderBmp.Width, renderBmp.Height, false, SurfaceFormat.Color);
                        Microsoft.Xna.Framework.Color[] colorData = new Microsoft.Xna.Framework.Color[renderBmp.Width * renderBmp.Height];
                        for (int y = 0; y < renderBmp.Height; y++)
                            for (int x = 0; x < renderBmp.Width; x++) {
                                System.Drawing.Color c = renderBmp.GetPixel(x, y);
                                colorData[y * renderBmp.Width + x] = new Microsoft.Xna.Framework.Color(c.R, c.G, c.B, c.A);
                            }
                        tex.SetData(colorData);
                        TextureCache[text] = tex;
                        return tex;
                    }
                }
            } catch { return null; }
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public static class Patch_DrawString1
    {
        static bool Prefix(SpriteBatch __instance, string text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text)) { Hook.FoundStrings.Add(text); Hook.Translations[text] = text; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(text, out string translated) && text != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(text, position), color); return false; }
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public static class Patch_DrawString2
    {
        static bool Prefix(SpriteBatch __instance, string text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth)
        {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text)) { Hook.FoundStrings.Add(text); Hook.Translations[text] = text; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(text, out string translated) && text != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(text, position), null, color, rotation, origin, scale, effects, layerDepth); return false; }
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public static class Patch_DrawString3
    {
        static bool Prefix(SpriteBatch __instance, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            if (text == null || text.Length == 0) return true;
            string str = text.ToString();
            if (!Hook.FoundStrings.Contains(str)) { Hook.FoundStrings.Add(str); Hook.Translations[str] = str; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(str, out string translated) && str != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(str, position), color); return false; }
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public static class Patch_DrawString4
    {
        static bool Prefix(SpriteBatch __instance, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth)
        {
            if (text == null || text.Length == 0) return true;
            string str = text.ToString();
            if (!Hook.FoundStrings.Contains(str)) { Hook.FoundStrings.Add(str); Hook.Translations[str] = str; Hook.SaveStrings(); }
            if (Hook.Translations.TryGetValue(str, out string translated) && str != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                if (tex != null) { __instance.Draw(tex, Hook.AdjustPosition(str, position), null, color, rotation, origin, scale, effects, layerDepth); return false; }
            }
            return true;
        }
    }
}
