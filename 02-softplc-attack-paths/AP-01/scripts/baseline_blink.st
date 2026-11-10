PROGRAM BlinkTest
    VAR
        Counter : INT := 0;
        LedOutput : BOOL := FALSE;
    END_VAR

    Counter := Counter + 1;
    IF Counter >= 10 THEN
        LedOutput := NOT LedOutput;
        Counter := 0;
    END_IF;
END_PROGRAM

CONFIGURATION Config0
    RESOURCE Res0 ON PLC
        TASK TaskMain(INTERVAL := T#500ms, PRIORITY := 0);
        PROGRAM Inst0 WITH TaskMain : BlinkTest;
    END_RESOURCE
END_CONFIGURATION