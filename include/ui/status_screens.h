#pragma once

void statusScreenPortal();
void statusScreenConnectFailed();
void statusScreenWifiReset();

/** Splash shown on boot; replace with a bitmap logo if desired. */
void statusScreenSplash();

/** Saved-network connect animation (call Tick until connect finishes). */
void statusScreenConnectingBegin(const char* ssid);
void statusScreenConnectingTick();
