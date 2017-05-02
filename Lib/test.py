def moveable_window_test():
    import unity_util
    import UnityEngine
    import GameCursor, CameraControl
    from UnityEngine import GUI, GUILayout, GUIStyle, GUIUtility, Screen, Rect, Vector3, Input, KeyCode
    from UnityEngine import Event, EventType, WaitForSeconds, GameObject
    import System
    
    unity_util.clean_behaviors()
    
    class Controller():
        def __init__(self):
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
                        
            def EnableCamera(value):
                if self.lastCameraState != value:
                    self.lastCameraState = value
                    if self.cameraControl:
                        self.cameraControl.enabled = value
                    self.gameCursor.enabled = value
                    
            def FuncWindowGUI(windowid):
                #Workaround mouse/camera issues when dragging window
                if GUIUtility.hotControl == 0:
                    EnableCamera(True)
                if Event.current.type == EventType.MouseDown:
                    GUI.FocusControl("")
                    GUI.FocusWindow(windowid)
                    EnableCamera(False)
                
                with GUILayout.VerticalScope("Group", GUI.skin.window):
                    GUILayout.Label(str(self.counter))
                    GUILayout.Label(str(self.windowRect))
                    self.show_buttons = GUILayout.Toggle(self.show_buttons, "Buttons")
                    if self.show_buttons:
                        if GUILayout.Button("Click me"):
                            print "clicked"
                        if GUILayout.Button("Slow Timer"):
                            self.component.StartCoroutine( self.RunSlowTimer() )
                        if GUILayout.Button("Close"):
                            if self.gameObject: 
                                UnityEngine.Object.DestroyObject(self.gameObject)
                GUI.DragWindow()
            self.windowCallback = GUI.WindowFunction(FuncWindowGUI)
                
        def Start(self):
            #self.useGUILayout = True
            if self.cameraControl == None:
                self.cameraControl = GameObject.Find('StudioCamera/Main Camera').GetComponent[CameraControl]()
            if self.gameCursor == None:
                self.gameCursor = UnityEngine.Object.FindObjectOfType[GameCursor]()
            
        def OnGUI(self):
            if not self.visible: return
            self.windowRect = GUI.Window(0, self.windowRect, self.windowCallback, "Window")
            
        def Update(self):
            # Update is called less so better place to check keystate
            if Input.GetKeyDown(KeyCode.F8):
                # unity sucks for checking meta keys
                ctrl, alt, shift = unity_util.metakey_state()
                if ctrl and not alt and not shift:
                    self.visible = not self.visible
                
        def RunSlowTimer(self):
            for i in range(1,10):
                self.counter = self.counter + 1
                yield WaitForSeconds(1)
            yield None
    
    return unity_util.create_gui_behavior(Controller)

    
    
def behavior_test():
    import unity_util
    import UnityEngine
    from UnityEngine import GUI, GUILayout, Screen, Rect, Input, KeyCode, WaitForSeconds
    import System
    unity_util.clean_behaviors()
    
    class DemoMessage():
        def __init__(self):
            self.color = UnityEngine.Color.white
            self.counter = 1
            self.options = System.Array.CreateInstance(UnityEngine.GUILayoutOption, 0)
            self.show_buttons = False
            self.gameObject = None # will be assigned if exists as member
            self.component = None # will be assigned if exists as member
            self.visible = True
            #print "Called when object is created"
            
        def Update(self):
            # Update is called less so better place to check keystate
            if Input.GetKeyDown(KeyCode.F8):
                # unity sucks for checking meta keys
                ctrl, alt, shift = unity_util.metakey_state()
                if ctrl and not alt and not shift:
                    self.visible = not self.visible
                    
        def OnGUI(self):
            if not self.visible: return
            
            #self.counter = self.counter + 1
            try:
                GUI.BeginGroup(Rect (Screen.width / 2 - 50, Screen.height / 2 - 50, 400, 400))
                GUI.color = UnityEngine.Color.white
                with GUILayout.VerticalScope("Group", GUI.skin.window):
                    GUILayout.Label(str(self.counter))
                    self.show_buttons = GUILayout.Toggle(self.show_buttons, "Buttons")
                    if self.show_buttons:
                        if GUILayout.Button("Click me"):
                            print "clicked"
                        if GUILayout.Button("Slow Timer"):
                            self.component.StartCoroutine( self.RunSlowTimer() )
                        if GUILayout.Button("Close"):
                            if self.gameObject: 
                                UnityEngine.Object.DestroyObject(self.gameObject)
            except:
                pass
            GUI.EndGroup()
                
        def RunSlowTimer(self):
            for i in range(1,10):
                self.counter = self.counter + 1
                yield WaitForSeconds(1)
            yield None
            
            
        def __del__(self):
            #print "Called when object is garbage collected"
            pass
    
    return unity_util.create_gui_behavior(DemoMessage)