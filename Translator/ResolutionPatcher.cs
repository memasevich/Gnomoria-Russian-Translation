using System;
using System.Runtime.InteropServices;
using HarmonyLib;

namespace GnomoriaTranslator
{
    public static class ResolutionPatcher
    {
        [DllImport("user32.dll")]
        private static extern bool SetProcessDPIAware();

        public static void Patch(Harmony harmony)
        {
            try
            {
                // Включаем DPI-Awareness для корректной работы на мониторах с высоким разрешением (High-DPI)
                try
                {
                    SetProcessDPIAware();
                    Hook.Log("DPI Awareness enabled successfully. Native resolutions unlocked!");
                }
                catch (Exception ex)
                {
                    Hook.Log("Failed to set DPI Awareness: " + ex.Message);
                }
            }
            catch (Exception ex)
            {
                Hook.Log("ResolutionPatcher Error: " + ex.ToString());
            }
        }
    }
}
