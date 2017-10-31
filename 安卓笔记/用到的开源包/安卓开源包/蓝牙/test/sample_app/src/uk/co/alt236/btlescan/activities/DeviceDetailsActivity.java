package uk.co.alt236.btlescan.activities;

import android.content.Intent;
import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;
import android.view.Menu;
import android.view.MenuItem;
import android.view.View;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;

import com.commonsware.cwac.merge.MergeAdapter;

import java.util.Collection;
import java.util.Locale;

import butterknife.Bind;
import butterknife.ButterKnife;
import uk.co.alt236.bluetoothlelib.device.BluetoothLeDevice;
import uk.co.alt236.bluetoothlelib.device.BluetoothService;
import uk.co.alt236.bluetoothlelib.device.adrecord.AdRecord;
import uk.co.alt236.bluetoothlelib.device.beacon.BeaconType;
import uk.co.alt236.bluetoothlelib.device.beacon.BeaconUtils;
import uk.co.alt236.bluetoothlelib.device.beacon.ibeacon.IBeaconManufacturerData;
import uk.co.alt236.bluetoothlelib.resolvers.CompanyIdentifierResolver;
import uk.co.alt236.bluetoothlelib.util.AdRecordUtils;
import uk.co.alt236.bluetoothlelib.util.ByteUtils;
import uk.co.alt236.btlescan.R;
import uk.co.alt236.btlescan.util.TimeFormatter;

public class DeviceDetailsActivity extends AppCompatActivity {
    public static final String EXTRA_DEVICE = "extra_device";
    @Bind(android.R.id.list)
    protected ListView mList;
    @Nullable
    @Bind(android.R.id.empty)
    protected View mEmpty;
    private BluetoothLeDevice mDevice;

    private void appendAdRecordView(final MergeAdapter adapter, final String title, final AdRecord record) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_adrecord, null);
        final TextView tvString = (TextView) lt.findViewById(R.id.data_as_string);
        final TextView tvArray = (TextView) lt.findViewById(R.id.data_as_array);
        final TextView tvTitle = (TextView) lt.findViewById(R.id.title);

        tvTitle.setText(title);
        tvString.setText("'" + AdRecordUtils.getRecordDataAsString(record) + "'");
        tvArray.setText("'" + ByteUtils.byteArrayToHexString(record.getData()) + "'");

        adapter.addView(lt);
    }

    private void appendDeviceInfo(final MergeAdapter adapter, final BluetoothLeDevice device) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_device_info, null);
        final TextView tvName = (TextView) lt.findViewById(R.id.deviceName);
        final TextView tvAddress = (TextView) lt.findViewById(R.id.deviceAddress);
        final TextView tvClass = (TextView) lt.findViewById(R.id.deviceClass);
        final TextView tvMajorClass = (TextView) lt.findViewById(R.id.deviceMajorClass);
        final TextView tvServices = (TextView) lt.findViewById(R.id.deviceServiceList);
        final TextView tvBondingState = (TextView) lt.findViewById(R.id.deviceBondingState);

        tvName.setText(device.getName());
        tvAddress.setText(device.getAddress());
        tvClass.setText(device.getBluetoothDeviceClassName());
        tvMajorClass.setText(device.getBluetoothDeviceMajorClassName());
        tvBondingState.setText(device.getBluetoothDeviceBondState());

        final String supportedServices;
        if(device.getBluetoothDeviceKnownSupportedServices().isEmpty()){
            supportedServices = getString(R.string.no_known_services);
        } else {
            final StringBuilder sb = new StringBuilder();

            for(final BluetoothService service : device.getBluetoothDeviceKnownSupportedServices()){
                if(sb.length() > 0){
                    sb.append(", ");
                }

                sb.append(service);
            }
            supportedServices = sb.toString();
        }

        tvServices.setText(supportedServices);

        adapter.addView(lt);
    }

    private void appendHeader(final MergeAdapter adapter, final String title) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_header, null);
        final TextView tvTitle = (TextView) lt.findViewById(R.id.title);
        tvTitle.setText(title);

        adapter.addView(lt);
    }

    private void appendIBeaconInfo(final MergeAdapter adapter, final IBeaconManufacturerData iBeaconData) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_ibeacon_details, null);
        final TextView tvCompanyId = (TextView) lt.findViewById(R.id.companyId);
        final TextView tvAdvert = (TextView) lt.findViewById(R.id.advertisement);
        final TextView tvUUID = (TextView) lt.findViewById(R.id.uuid);
        final TextView tvMajor = (TextView) lt.findViewById(R.id.major);
        final TextView tvMinor = (TextView) lt.findViewById(R.id.minor);
        final TextView tvTxPower = (TextView) lt.findViewById(R.id.txpower);

        tvCompanyId.setText(
                CompanyIdentifierResolver.getCompanyName(iBeaconData.getCompanyIdentifier(), getString(R.string.unknown))
                        + " (" + hexEncode(iBeaconData.getCompanyIdentifier()) + ")");
        tvAdvert.setText(iBeaconData.getIBeaconAdvertisement() + " (" + hexEncode(iBeaconData.getIBeaconAdvertisement()) + ")");
        tvUUID.setText(iBeaconData.getUUID());
        tvMajor.setText(iBeaconData.getMajor() + " (" + hexEncode(iBeaconData.getMajor()) + ")");
        tvMinor.setText(iBeaconData.getMinor() + " (" + hexEncode(iBeaconData.getMinor()) + ")");
        tvTxPower.setText(iBeaconData.getCalibratedTxPower() + " (" + hexEncode(iBeaconData.getCalibratedTxPower()) + ")");

        adapter.addView(lt);
    }

    private void appendRssiInfo(final MergeAdapter adapter, final BluetoothLeDevice device) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_rssi_info, null);
        final TextView tvFirstTimestamp = (TextView) lt.findViewById(R.id.firstTimestamp);
        final TextView tvFirstRssi = (TextView) lt.findViewById(R.id.firstRssi);
        final TextView tvLastTimestamp = (TextView) lt.findViewById(R.id.lastTimestamp);
        final TextView tvLastRssi = (TextView) lt.findViewById(R.id.lastRssi);
        final TextView tvRunningAverageRssi = (TextView) lt.findViewById(R.id.runningAverageRssi);

        tvFirstTimestamp.setText(formatTime(device.getFirstTimestamp()));
        tvFirstRssi.setText(formatRssi(device.getFirstRssi()));
        tvLastTimestamp.setText(formatTime(device.getTimestamp()));
        tvLastRssi.setText(formatRssi(device.getRssi()));
        tvRunningAverageRssi.setText(formatRssi(device.getRunningAverageRssi()));

        adapter.addView(lt);
    }

    private void appendSimpleText(final MergeAdapter adapter, final byte[] data) {
        appendSimpleText(adapter, ByteUtils.byteArrayToHexString(data));
    }

    private void appendSimpleText(final MergeAdapter adapter, final String data) {
        final LinearLayout lt = (LinearLayout) getLayoutInflater().inflate(R.layout.list_item_view_textview, null);
        final TextView tvData = (TextView) lt.findViewById(R.id.data);

        tvData.setText(data);

        adapter.addView(lt);
    }


    private String formatRssi(final double rssi) {
        return getString(R.string.formatter_db, String.valueOf(rssi));
    }

    private String formatRssi(final int rssi) {
        return getString(R.string.formatter_db, String.valueOf(rssi));
    }

    @Override
    protected void onCreate(final Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_details);
        ButterKnife.bind(this);

        mList.setEmptyView(mEmpty);

        mDevice = getIntent().getParcelableExtra(EXTRA_DEVICE);

        pupulateDetails(mDevice);
    }

    @Override
    public boolean onCreateOptionsMenu(final Menu menu) {
        getMenuInflater().inflate(R.menu.details, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(final MenuItem item) {
        switch (item.getItemId()) {
            case R.id.menu_connect:

                final Intent intent = new Intent(this, DeviceControlActivity.class);
                intent.putExtra(DeviceControlActivity.EXTRA_DEVICE, mDevice);

                startActivity(intent);

                break;
        }
        return true;
    }

    private void pupulateDetails(final BluetoothLeDevice device) {
        final MergeAdapter adapter = new MergeAdapter();

        if (device == null) {
            appendHeader(adapter, getString(R.string.header_device_info));
            appendSimpleText(adapter, getString(R.string.invalid_device_data));
        } else {
            appendHeader(adapter, getString(R.string.header_device_info));
            appendDeviceInfo(adapter, device);

            appendHeader(adapter, getString(R.string.header_rssi_info));
            appendRssiInfo(adapter, device);

            appendHeader(adapter, getString(R.string.header_scan_record));
            appendSimpleText(adapter, device.getScanRecord());

            final Collection<AdRecord> adRecords = device.getAdRecordStore().getRecordsAsCollection();
            if (adRecords.size() > 0) {
                appendHeader(adapter, getString(R.string.header_raw_ad_records));

                for (final AdRecord record : adRecords) {

                    appendAdRecordView(
                            adapter,
                            "#" + record.getType() + " " + record.getHumanReadableType(),
                            record);
                }
            }

            final boolean isIBeacon = BeaconUtils.getBeaconType(device) == BeaconType.IBEACON;
            if (isIBeacon) {
                final IBeaconManufacturerData iBeaconData = new IBeaconManufacturerData(device);
                appendHeader(adapter, getString(R.string.header_ibeacon_data));
                appendIBeaconInfo(adapter, iBeaconData);
            }

        }
        mList.setAdapter(adapter);
    }

    private static String formatTime(final long time) {
        return TimeFormatter.getIsoDateTime(time);
    }

    private static String hexEncode(final int integer) {
        return "0x" + Integer.toHexString(integer).toUpperCase(Locale.US);
    }
}
