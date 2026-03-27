@echo off
title QBO Sweep - God Complete v8.0
cd /d C:\Users\adm_r\Clients\intuit-boom
claude "Read dashboard/SWEEP_PLAYBOOK.md and dashboard/pending/SWEEP_ACTIVATION.md. Execute the playbook screen by screen. Use ONLY the credentials in SWEEP_ACTIVATION.md." --dangerously-skip-permissions
echo.
echo === SWEEP FINALIZADO ===
pause
