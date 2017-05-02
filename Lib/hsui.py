class BaseController():
    def __init__(self):
        from UnityEngine import Screen, Rect
        
        self.gameObject = None # will be assigned if exists as member
        self.component = None # will be assigned if exists as member
        self.counter = 1
        self.show_buttons = False
        self.visible = True
        self.style = None
        self.cameraControl = None
        self.windowRect = Rect (Screen.width / 2 - 50, Screen.height / 2 - 50, 400, 400)
        self.lastCameraState = True
        self.gameCursor = None
        self.windowName = "Window"

    def EnableCamera(self, value):
        if self.lastCameraState != value:
            self.lastCameraState = value
            if self.cameraControl:
                self.cameraControl.enabled = value
            self.gameCursor.enabled = value
        
    def ResetWindow(self, windowid):
        from UnityEngine import GUI, GUIUtility
        from UnityEngine import Event, EventType
        #Workaround mouse/camera issues when dragging window
        if GUIUtility.hotControl == 0:
            self.EnableCamera(True)
        if Event.current.type == EventType.MouseDown:
            GUI.FocusControl("")
            GUI.FocusWindow(windowid)
            self.EnableCamera(False)
        
    def Start(self):
        import UnityEngine
        import GameCursor, CameraControl
        from UnityEngine import GameObject
    
        #self.useGUILayout = True
        if self.cameraControl == None:
            self.cameraControl = GameObject.Find('StudioCamera/Main Camera').GetComponent[CameraControl]()
        if self.gameCursor == None:
            self.gameCursor = UnityEngine.Object.FindObjectOfType[GameCursor]()
        
    def OnGUI(self):
        from UnityEngine import GUI
        if not self.visible: return
        self.windowRect = GUI.Window(0, self.windowRect, self.windowCallback, self.windowName)
    
    def Update(self):
        import unity_util
        from UnityEngine import Input, KeyCode
        # Update is called less so better place to check keystate
        if Input.GetKeyDown(KeyCode.F8):
            # unity sucks for checking meta keys
            ctrl, alt, shift = unity_util.metakey_state()
            if ctrl and not alt and not shift:
                self.visible = not self.visible

def capture_window():
    import unity_util
    import UnityEngine
    import GameCursor, CameraControl
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
    from UnityEngine import Event, EventType, WaitForSeconds, GameObject
    import System
    
    unity_util.clean_behaviors()
    
    class Controller(BaseController):
        def __init__(self):
            BaseController.__init__(self)
            
            self.windowName = 'Python'
            self.windowRect = Rect (Screen.width - 100 - 10, 0, 100, 100)
            
            def FuncWindowGUI(windowid):
                self.ResetWindow(windowid) #required for dragging
                
                self.show_buttons = GUILayout.Toggle(self.show_buttons, "Show")
                if self.show_buttons:
                    if GUILayout.Button("Capture"):
                        import hs
                        hs.capture_noblock()
                    #if GUILayout.Button("Close"):
                    #    if self.gameObject: 
                    #        UnityEngine.Object.DestroyObject(self.gameObject)
                GUI.DragWindow()
            self.windowCallback = GUI.WindowFunction(FuncWindowGUI)
            
        def Start(self):
            BaseController.Start(self)
            
        def OnGUI(self):
            r = self.windowRect
            self.windowRect = Rect(r.x, r.y, r.width, 70 if self.show_buttons else 50)
            BaseController.OnGUI(self)
            
        def Update(self):
            BaseController.Update(self)
            
    return unity_util.create_gui_behavior(Controller)
