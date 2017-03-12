from hs import unity as _unity

@_unity
def Capture(_path='', _alpha=True, _width=0, _height=0, _rate=1):
    import System
    from System import *
    from System.IO import *
    from UnityEngine import *
    from UnityEngine import Object as Object
    
    width = (_width if _width != 0 else Screen.width) * _rate
    height = (_height if _height != 0 else Screen.height) * _rate
    tex = Texture2D(width, height, TextureFormat.RGB24 if not _alpha else TextureFormat.ARGB32, False)
    tex2 = Texture2D(width, height, TextureFormat.RGB24 if not _alpha else TextureFormat.ARGB32, False)
    if QualitySettings.antiAliasing != 0:
        rt = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20, RenderTextureFormat.Default, RenderTextureReadWrite.Default, QualitySettings.antiAliasing)
        rt2 = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20, RenderTextureFormat.Default, RenderTextureReadWrite.Default, QualitySettings.antiAliasing)
    else:
        rt = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20)
        rt2 = RenderTexture.GetTemporary(width, height, 0x18 if not _alpha else 0x20)
    #RenderCam = Camera.main
    RenderCam = Manager.Studio.Instance.MainCamera
    backRenderTexture = RenderCam.targetTexture
    backRect = RenderCam.rect
    oldBackground = RenderCam.backgroundColor
    oldFlags = RenderCam.clearFlags
    RenderCam.backgroundColor = Color(Single(1), Single(1), Single(1), Single(1))
    RenderCam.clearFlags = CameraClearFlags.Color
    RenderCam.targetTexture = rt
    RenderCam.Render()
    RenderCam.targetTexture = backRenderTexture
    RenderCam.rect = backRect
    RenderTexture.active = rt
    tex.ReadPixels(Rect(Single(0), Single(0), width, height), 0, 0)
    tex.Apply()
    RenderTexture.active = None
    RenderCam.backgroundColor = Color(Single(0), Single(0), Single(0), Single(1))
    RenderCam.clearFlags = CameraClearFlags.Color
    RenderCam.targetTexture = rt2
    RenderCam.Render()
    RenderCam.targetTexture = backRenderTexture
    RenderCam.rect = backRect
    RenderTexture.active = rt2
    tex2.ReadPixels(Rect(Single(0), Single(0), width, height), 0, 0)
    tex2.Apply()
    RenderTexture.active = None
    RenderCam.backgroundColor = oldBackground
    RenderCam.clearFlags = oldFlags
    cols1 = tex.GetPixels()
    cols2 = tex2.GetPixels()
    for i in xrange(0,cols1.Length-1):
        c1 = cols1[i]
        c2 = cols2[i]
        if c1 == c2: continue
        #var a = 1.0f - Math.Min(Math.Abs(c1.r - c2.r), Math.Min(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)));
        #var a = 1.0f - (Math.Abs(c1.r - c2.r) + Math.Abs(c1.g - c2.g) + Math.Abs(c1.b - c2.b)) / 3.0f ;
        a = Single(1) - Math.Max(Math.Abs(c1.r - c2.r), Math.Max(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)))
        cols1[i] = Color(c1.r, c1.g, c1.b, a)
    tex.SetPixels(cols1)
    tex.Apply()
    bytes = tex.EncodeToPNG()
    Object.Destroy(tex)
    RenderTexture.ReleaseTemporary(rt)
    RenderTexture.ReleaseTemporary(rt2)
    tex = None
    if str.Empty == _path:
        import UserData
        _path = UserData.Create("cap")
        fileName = YS_Assist.GetDateTimeString(DateTime.Now, "", True, True, True, True, True, True, True)
        _path = Path.GetFullPath(Path.Combine(_path, fileName + ".png"))
        Console.WriteLine("Capture: " + _path)
    File.WriteAllBytes(_path, bytes)
    return True

