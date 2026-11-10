PROGRAM MaliciousBlink
    VAR
        Counter : INT := 0;
    END_VAR
    VAR
        ExploitTrigger AT %MW0 : INT;
    END_VAR

    Counter := Counter + 1;
    IF Counter >= 5 THEN
        IF ExploitTrigger = 0 THEN
            ExploitTrigger := 1;
        ELSE
            ExploitTrigger := 0;
        END_IF;
        Counter := 0;
    END_IF;
END_PROGRAM

CONFIGURATION Config0
    RESOURCE Res0 ON PLC
        TASK TaskMain(INTERVAL := T#200ms, PRIORITY := 0);
        PROGRAM Inst0 WITH TaskMain : MaliciousBlink;
    END_RESOURCE
END_CONFIGURATION