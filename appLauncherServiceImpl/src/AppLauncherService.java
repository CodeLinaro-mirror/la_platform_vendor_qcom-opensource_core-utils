// Copyright (c) Qualcomm Technologies, Inc. and/or its subsidiaries.
// SPDX-License-Identifier: BSD-3-Clause-Clear

package vendor.qti.applauncher;

import android.util.Slog;
import android.os.RemoteException;
import vendor.qti.appLauncherService.IAppLauncherService;
import android.content.ComponentName;
import android.content.Context;
import android.content.Intent;
import android.app.ActivityManager;
import android.os.UserHandle;


public class AppLauncherService extends IAppLauncherService.Stub {

    private static final String TAG = "AppLauncherService";
    private final Context mContext;

    public AppLauncherService(Context context) {
        mContext = context;
        Slog.d(TAG,"*** AppLauncherService starting ***");
    }

    public void startService(String pkgName, String serviceName) throws RemoteException {

        if (pkgName == null || serviceName == null) {
            Slog.e(TAG,"Incorrect pkgName/serviceName received in startService");
            return;
        }

        Slog.d(TAG,"startService called for pkgName = " + pkgName + " serviceName = " + serviceName);

        try {
            Intent intent = new Intent();
            if (intent != null){
                intent.setComponent(new ComponentName(pkgName, pkgName + "." + serviceName));
                mContext.startServiceAsUser(intent, UserHandle.of(ActivityManager.getCurrentUser()));
            } else {
                Slog.e(TAG,"No launch intent found for package :" + pkgName + "." + serviceName);
            }
        } catch (Exception e){
            Slog.e(TAG, "Failed to launch app" + pkgName, e);
            throw new RemoteException("Failed to launch app " + pkgName + " error: " + e);
        }
    }

    public void stopService(String pkgName, String serviceName) throws RemoteException {

        if (pkgName == null || serviceName == null) {
            Slog.e(TAG,"Incorrect pkgName/serviceName received in stopService");
            return;
        }

        Slog.d(TAG,"stopService called for pkgName = " + pkgName + " serviceName = " + serviceName);

        try {
            Intent intent = new Intent();
            if (intent != null){
                intent.setComponent(new ComponentName(pkgName, pkgName + "." + serviceName));
                boolean isStopped = mContext.stopService(intent);
                if (isStopped) {
                    Slog.d(TAG, "Successfully stopped service: " + serviceName + "for package: " + pkgName);
                } else {
                    Slog.e(TAG, "Failed to stop service: " + serviceName + "for package: " + pkgName);
                }
            } else{
                Slog.e(TAG,"No launch intent found for package :" + pkgName + "." + serviceName);
            }
        } catch (Exception e){
            Slog.e(TAG, "Failed to stop service" + pkgName, e);
            throw new RemoteException("Failed to stop service " + pkgName + " error: " + e);
        }

    }

    @Override
    public int getInterfaceVersion() {
        return this.VERSION;
    }

    @Override
    public String getInterfaceHash() {
        return this.HASH;
    }
}