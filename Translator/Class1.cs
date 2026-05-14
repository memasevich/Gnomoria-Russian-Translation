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
                if (File.Exists(LogPath))
                {
                    string json = File.ReadAllText(LogPath);
                    Translations = Newtonsoft.Json.JsonConvert.DeserializeObject<Dictionary<string, string>>(json) ?? new Dictionary<string, string>();
                    foreach(var k in Translations.Keys) FoundStrings.Add(k);
                }

                var harmony = new Harmony("com.lecoo.gnomoriatranslator");
                harmony.PatchAll();
            }
            catch { }
        }

        public static void SaveStrings()
        {
            try
            {
                var json = Newtonsoft.Json.JsonConvert.SerializeObject(Translations, Newtonsoft.Json.Formatting.Indented);
                File.WriteAllText(LogPath, json);
            }
            catch { }
        }

        public static Texture2D GetTextTexture(GraphicsDevice device, string text)
        {
            if (TextureCache.TryGetValue(text, out Texture2D tex)) return tex;

            using (Bitmap bmp = new Bitmap(1, 1))
            using (Graphics g = Graphics.FromImage(bmp))
            {
                SizeF size = g.MeasureString(text, SysFont);
                int width = (int)Math.Ceiling(size.Width);
                int height = (int)Math.Ceiling(size.Height);
                if (width <= 0) width = 1;
                if (height <= 0) height = 1;

                using (Bitmap renderBmp = new Bitmap(width, height))
                using (Graphics renderG = Graphics.FromImage(renderBmp))
                {
                    renderG.SmoothingMode = SmoothingMode.HighQuality;
                    renderG.TextRenderingHint = TextRenderingHint.AntiAliasGridFit;
                    renderG.Clear(System.Drawing.Color.Transparent);
                    renderG.DrawString(text, SysFont, SysBrush, 0, 0);

                    tex = new Texture2D(device, width, height, false, SurfaceFormat.Color);
                    Microsoft.Xna.Framework.Color[] colorData = new Microsoft.Xna.Framework.Color[width * height];
                    for (int y = 0; y < height; y++)
                    {
                        for (int x = 0; x < width; x++)
                        {
                            System.Drawing.Color c = renderBmp.GetPixel(x, y);
                            colorData[y * width + x] = new Microsoft.Xna.Framework.Color(c.R, c.G, c.B, c.A);
                        }
                    }
                    tex.SetData(colorData);
                    TextureCache[text] = tex;
                    return tex;
                }
            }
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public class Patch_DrawString1
    {
        static bool Prefix(SpriteBatch __instance, SpriteFont spriteFont, string text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text))
            {
                Hook.FoundStrings.Add(text);
                Hook.Translations[text] = text;
                Hook.SaveStrings();
                return true;
            }

            if (Hook.Translations.TryGetValue(text, out string translated) && text != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                __instance.Draw(tex, position, color);
                return false;
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(string), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public class Patch_DrawString2
    {
        static bool Prefix(SpriteBatch __instance, SpriteFont spriteFont, string text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth)
        {
            if (string.IsNullOrEmpty(text)) return true;
            if (!Hook.FoundStrings.Contains(text))
            {
                Hook.FoundStrings.Add(text);
                Hook.Translations[text] = text;
                Hook.SaveStrings();
                return true;
            }

            if (Hook.Translations.TryGetValue(text, out string translated) && text != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                __instance.Draw(tex, position, null, color, rotation, origin, scale, effects, layerDepth);
                return false;
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color) })]
    public class Patch_DrawString3
    {
        static bool Prefix(SpriteBatch __instance, SpriteFont spriteFont, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color)
        {
            if (text == null || text.Length == 0) return true;
            string str = text.ToString();
            if (!Hook.FoundStrings.Contains(str))
            {
                Hook.FoundStrings.Add(str);
                Hook.Translations[str] = str;
                Hook.SaveStrings();
                return true;
            }

            if (Hook.Translations.TryGetValue(str, out string translated) && str != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                __instance.Draw(tex, position, color);
                return false;
            }
            return true;
        }
    }

    [HarmonyPatch(typeof(SpriteBatch), "DrawString", new Type[] { typeof(SpriteFont), typeof(System.Text.StringBuilder), typeof(Vector2), typeof(Microsoft.Xna.Framework.Color), typeof(float), typeof(Vector2), typeof(float), typeof(SpriteEffects), typeof(float) })]
    public class Patch_DrawString4
    {
        static bool Prefix(SpriteBatch __instance, SpriteFont spriteFont, System.Text.StringBuilder text, Vector2 position, Microsoft.Xna.Framework.Color color, float rotation, Vector2 origin, float scale, SpriteEffects effects, float layerDepth)
        {
            if (text == null || text.Length == 0) return true;
            string str = text.ToString();
            if (!Hook.FoundStrings.Contains(str))
            {
                Hook.FoundStrings.Add(str);
                Hook.Translations[str] = str;
                Hook.SaveStrings();
                return true;
            }

            if (Hook.Translations.TryGetValue(str, out string translated) && str != translated)
            {
                Texture2D tex = Hook.GetTextTexture(__instance.GraphicsDevice, translated);
                __instance.Draw(tex, position, null, color, rotation, origin, scale, effects, layerDepth);
                return false;
            }
            return true;
        }
    }
}