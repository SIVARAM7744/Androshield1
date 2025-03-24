import os
import pandas as pd
from androguard.misc import AnalyzeAPK

# Đọc dataset hiện có từ data.csv
df_existing = pd.read_csv('data.csv')

# Danh sách các đặc trưng (permissions) trong mô hình
features = [
    'android.permission.GET_ACCOUNTS', 'com.sonyericsson.home.permission.BROADCAST_BADGE',
    'android.permission.READ_PROFILE', 'android.permission.MANAGE_ACCOUNTS',
    'android.permission.WRITE_SYNC_SETTINGS', 'android.permission.READ_EXTERNAL_STORAGE',
    'android.permission.RECEIVE_SMS', 'com.android.launcher.permission.READ_SETTINGS',
    'android.permission.WRITE_SETTINGS', 'com.google.android.providers.gsf.permission.READ_GSERVICES',
    'android.permission.DOWNLOAD_WITHOUT_NOTIFICATION', 'android.permission.GET_TASKS',
    'android.permission.WRITE_EXTERNAL_STORAGE', 'android.permission.RECORD_AUDIO',
    'com.huawei.android.launcher.permission.CHANGE_BADGE', 'com.oppo.launcher.permission.READ_SETTINGS',
    'android.permission.CHANGE_NETWORK_STATE', 'com.android.launcher.permission.INSTALL_SHORTCUT',
    'android.permission.android.permission.READ_PHONE_STATE', 'android.permission.CALL_PHONE',
    'android.permission.WRITE_CONTACTS', 'android.permission.READ_PHONE_STATE',
    'com.samsung.android.providers.context.permission.WRITE_USE_APP_FEATURE_SURVEY',
    'android.permission.MODIFY_AUDIO_SETTINGS', 'android.permission.ACCESS_LOCATION_EXTRA_COMMANDS',
    'android.permission.INTERNET', 'android.permission.MOUNT_UNMOUNT_FILESYSTEMS',
    'com.majeur.launcher.permission.UPDATE_BADGE', 'android.permission.AUTHENTICATE_ACCOUNTS',
    'com.htc.launcher.permission.READ_SETTINGS', 'android.permission.ACCESS_WIFI_STATE',
    'android.permission.FLASHLIGHT', 'android.permission.READ_APP_BADGE',
    'android.permission.USE_CREDENTIALS', 'android.permission.CHANGE_CONFIGURATION',
    'android.permission.READ_SYNC_SETTINGS', 'android.permission.BROADCAST_STICKY',
    'com.anddoes.launcher.permission.UPDATE_COUNT', 'com.android.alarm.permission.SET_ALARM',
    'com.google.android.c2dm.permission.RECEIVE', 'android.permission.KILL_BACKGROUND_PROCESSES',
    'com.sonymobile.home.permission.PROVIDER_INSERT_BADGE', 'com.sec.android.provider.badge.permission.READ',
    'android.permission.WRITE_CALENDAR', 'android.permission.SEND_SMS',
    'com.huawei.android.launcher.permission.WRITE_SETTINGS', 'android.permission.REQUEST_INSTALL_PACKAGES',
    'android.permission.SET_WALLPAPER_HINTS', 'android.permission.SET_WALLPAPER',
    'com.oppo.launcher.permission.WRITE_SETTINGS', 'android.permission.RESTART_PACKAGES',
    'me.everything.badger.permission.BADGE_COUNT_WRITE', 'android.permission.ACCESS_MOCK_LOCATION',
    'android.permission.ACCESS_COARSE_LOCATION', 'android.permission.READ_LOGS',
    'com.google.android.gms.permission.ACTIVITY_RECOGNITION', 'com.amazon.device.messaging.permission.RECEIVE',
    'android.permission.SYSTEM_ALERT_WINDOW', 'android.permission.DISABLE_KEYGUARD',
    'android.permission.USE_FINGERPRINT', 'me.everything.badger.permission.BADGE_COUNT_READ',
    'android.permission.CHANGE_WIFI_STATE', 'android.permission.READ_CONTACTS',
    'com.android.vending.BILLING', 'android.permission.READ_CALENDAR',
    'android.permission.RECEIVE_BOOT_COMPLETED', 'android.permission.WAKE_LOCK',
    'android.permission.ACCESS_FINE_LOCATION', 'android.permission.BLUETOOTH',
    'android.permission.CAMERA', 'com.android.vending.CHECK_LICENSE',
    'android.permission.FOREGROUND_SERVICE', 'android.permission.BLUETOOTH_ADMIN',
    'android.permission.VIBRATE', 'android.permission.NFC',
    'android.permission.RECEIVE_USER_PRESENT', 'android.permission.CLEAR_APP_CACHE',
    'com.android.launcher.permission.UNINSTALL_SHORTCUT',
    # Các quyền mới bạn muốn thêm vào
    'com.sec.android.iap.permission.BILLING', 'com.htc.launcher.permission.UPDATE_SHORTCUT',
    'com.sec.android.provider.badge.permission.WRITE', 'android.permission.ACCESS_NETWORK_STATE',
    'com.google.android.finsky.permission.BIND_GET_INSTALL_REFERRER_SERVICE', 'com.huawei.android.launcher.permission.READ_SETTINGS',
    'android.permission.READ_SMS', 'android.permission.PROCESS_INCOMING_CALLS',
    # Cột Result sẽ có giá trị mặc định là 1
    'Result'
]

# Hàm trích xuất đặc trưng từ file APK
def extract_features_from_apk(apk_path):
    a, d, dx = AnalyzeAPK(apk_path)
    permissions = a.get_permissions()

    # Chuẩn bị vector đặc trưng dựa trên quyền
    vector = {feature: 1 if feature in permissions else 0 for feature in features}
    vector['Result'] = 0  # Gán Result = 1 vì đang trích xuất mã độc
    return vector

# Duyệt qua các tệp APK trong thư mục 'apks'
apk_dir = 'File apk test/Benign'  # Cập nhật đúng thư mục chứa tệp APK
apk_files = [f for f in os.listdir(apk_dir) if f.endswith('.apk')]

# Tạo DataFrame từ các APK mới
new_data = []
for apk_file in apk_files:
    apk_path = os.path.join(apk_dir, apk_file)
    feature_vector = extract_features_from_apk(apk_path)
    feature_vector['apk_name'] = apk_file  # Nếu bạn muốn giữ tên file APK
    new_data.append(feature_vector)

df_new = pd.DataFrame(new_data)

# Gộp dữ liệu cũ và mới
df_combined = pd.concat([df_existing, df_new], ignore_index=True)

# Xóa cột 'apk_name'
df_combined = df_combined.drop(columns=['apk_name'])

# Lưu DataFrame kết hợp vào 'data.csv'
df_combined.to_csv('data.csv', index=False)

print("Extraction completed and data saved to 'data.csv'")
