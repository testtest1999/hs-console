using System;
using System.IO;
using UnityEngine;
using Object = UnityEngine.Object;

namespace HS.Utility
{
    public class ScreenShot
    {
        public static bool PerformCapture(SSInfo ssinfo)
        {
            return PerformCapture(ssinfo.path, ssinfo.alpha, ssinfo.width, ssinfo.height, ssinfo.rate);
        }

        public static bool PerformCapture()
        {
            return PerformCapture("", true, 0, 0, 1);
        }

        public static bool PerformCapture(string path)
        {
            return PerformCapture(path, true, 0, 0, 1);
        }

        public static bool PerformCapture(string _path, bool _alpha, int _width, int _height, int _rate)
        {
            RenderTexture rt, rt2;
            var width = (_width != 0 ? _width : Screen.width)*_rate;
            var height = (_height != 0 ? _height : Screen.height)*_rate;
            var tex = new Texture2D(width, height, !_alpha ? TextureFormat.RGB24 : TextureFormat.ARGB32, false);
            var tex2 = new Texture2D(width, height, !_alpha ? TextureFormat.RGB24 : TextureFormat.ARGB32, false);
            if (QualitySettings.antiAliasing != 0)
            {
                rt = RenderTexture.GetTemporary(width, height, !_alpha ? 0x18 : 0x20,
                    RenderTextureFormat.Default, RenderTextureReadWrite.Default,
                    QualitySettings.antiAliasing);
                rt2 = RenderTexture.GetTemporary(width, height, !_alpha ? 0x18 : 0x20,
                    RenderTextureFormat.Default, RenderTextureReadWrite.Default,
                    QualitySettings.antiAliasing);
            }
            else
            {
                rt = RenderTexture.GetTemporary(width, height, !_alpha ? 0x18 : 0x20);
                rt2 = RenderTexture.GetTemporary(width, height, !_alpha ? 0x18 : 0x20);
            }
            var RenderCam = Camera.main;
            var backRenderTexture = RenderCam.targetTexture;
            var backRect = RenderCam.rect;

            var oldBackground = RenderCam.backgroundColor;
            var oldFlags = RenderCam.clearFlags;

            RenderCam.backgroundColor = new Color(1.0f, 1.0f, 1.0f, 1.0f);
            RenderCam.clearFlags = CameraClearFlags.Color;
            RenderCam.targetTexture = rt;
            RenderCam.Render();
            RenderCam.targetTexture = backRenderTexture;
            RenderCam.rect = backRect;
            RenderTexture.active = rt;
            tex.ReadPixels(new Rect(0f, 0f, width, height), 0, 0);
            tex.Apply();
            RenderTexture.active = null;

            RenderCam.backgroundColor = new Color(0.0f, 0.0f, 0.0f, 1.0f);
            RenderCam.clearFlags = CameraClearFlags.Color;
            RenderCam.targetTexture = rt2;
            RenderCam.Render();
            RenderCam.targetTexture = backRenderTexture;
            RenderCam.rect = backRect;
            RenderTexture.active = rt2;
            tex2.ReadPixels(new Rect(0f, 0f, width, height), 0, 0);
            tex2.Apply();
            RenderTexture.active = null;

            RenderCam.backgroundColor = oldBackground;
            RenderCam.clearFlags = oldFlags;


            var cols1 = tex.GetPixels();
            var cols2 = tex2.GetPixels();
            for (var i = 0; i < cols1.Length; ++i)
            {
                if (cols1[i] == cols2[i]) continue;

                var c1 = cols1[i];
                var c2 = cols2[i];
                //var a = 1.0f - Math.Min(Math.Abs(c1.r - c2.r), Math.Min(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)));
                //var a = 1.0f - (Math.Abs(c1.r - c2.r) + Math.Abs(c1.g - c2.g) + Math.Abs(c1.b - c2.b)) / 3.0f ;
                var a = 1.0f - Math.Max(Math.Abs(c1.r - c2.r), Math.Max(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)));
                cols1[i] = new Color(c1.r, c1.g, c1.b, a);
            }
            tex.SetPixels(cols1);
            tex.Apply();

            var bytes = tex.EncodeToPNG();
            Object.Destroy(tex);

            RenderTexture.ReleaseTemporary(rt);
            RenderTexture.ReleaseTemporary(rt2);
            tex = null;
            if (string.Empty == _path)
            {
                _path = UserData.Create("cap");
                var fileName = YS_Assist.GetDateTimeString(DateTime.Now, "", true, true, true, true, true, true, true);
                _path = Path.GetFullPath(Path.Combine(_path, fileName + ".png"));
                Console.WriteLine("Capture: " + _path);
            }
            File.WriteAllBytes(_path, bytes);
            return true;
        }
    }

    public class SSInfo
    {
        public bool alpha;
        public int height;
        public string path = string.Empty;
        public int rate = 1;
        public int width;

        public void Set(string _path, bool _alpha, int _width, int _height, int _rate)
        {
            path = _path;
            alpha = _alpha;
            width = _width;
            height = _height;
            rate = _rate;
        }
    }
}