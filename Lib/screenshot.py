from hs import unity as _unity

def capture_noblock(_path='', _alpha=True, autofit=True):
    import System
    import Manager
    from System import *
    from System.IO import *
    from UnityEngine import *
    from UnityEngine import Object as Object
    from UnityEngine import Time as Time
    width = Screen.width
    height = Screen.height
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
    RenderTexture.ReleaseTemporary(rt)
    RenderTexture.ReleaseTemporary(rt2)
    
    cols1 = tex.GetPixels()
    cols2 = tex2.GetPixels()
    x1, x2 = width, 0
    y1, y2 = height, 0
    
    for i in xrange(0,cols1.Length-1):
        c1 = cols1[i]
        c2 = cols2[i]
        a = 1.0
        if c1 != c2:
            a = Single(1) - Math.Max(Math.Abs(c1.r - c2.r), Math.Max(Math.Abs(c1.g - c2.g), Math.Abs(c1.b - c2.b)))
            cols1[i] = Color(c1.r, c1.g, c1.b, a)
        if autofit and a > 0.05:
            y = i // width
            x = i - y*width
            if x < x1: x1 = x
            if x > x2: x2 = x
            if y < y1: y1 = y
            if y > y2: y2 = y
    if autofit:
        def irnd(x):
            return x + x%2
        # add padding then truncate
        padding = 4
        x1,y1 = max(0, irnd(x1-padding)), max(0, irnd(y1-padding))
        x2,y2 = min(width, irnd(x2+padding)), min(height, irnd(y2+padding))
        Object.Destroy(tex)
        w,h = x2-x1, y2-y1
        tex = Texture2D(x2-x1, y2-y1, TextureFormat.ARGB32, False)
        cols = tex.GetPixels()
        for i in range(x1, x2):
            for j in range(y1, y2):
                cols[(j-y1)*w+(i-x1)] = cols1[j*width+i]
        tex.SetPixels(cols)
        tex.Apply()
    else:
        tex.SetPixels(cols1)
        tex.Apply()
    bytes = tex.EncodeToPNG()
    Object.Destroy(tex)
    tex = None
    if str.Empty == _path:
        import UserData, datetime
        _path = UserData.Create("cap")
        fileName = datetime.datetime.now().strftime('%Y%m%d%H%M%S%f')[:-3]
        _path = Path.GetFullPath(Path.Combine(_path, fileName + ".png"))
        Console.WriteLine("Capture: " + _path)
    File.WriteAllBytes(_path, bytes)
    return True

@_unity
def capture(_path='', _alpha=True, autofit=True):
    capture_noblock(_path, _alpha, autofit)