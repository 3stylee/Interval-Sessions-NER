MODEL_SCALER_INFO = {
	"data_min": [0.0, 24.0, 0.0, 0.612, 2.9, 0.0],
	"data_max": [18347.5, 4900.0, 436.0, 8.948, 12.0, 116.0],
}

def processData(data):
    processedData = [scaleRow([
        row['distance'],
        row['moving_time'],
        row['total_elevation_gain'],
        row['average_speed'],
        row['max_speed'],
        row['average_cadence'],
    ]) for row in data]
    return processedData

def scaleRow(row):
    scaledRow = []
    for index, value in enumerate(row):
        dataMin = MODEL_SCALER_INFO['data_min'][index]
        dataMax = MODEL_SCALER_INFO['data_max'][index]
        range_val = dataMax - dataMin

        # Apply Min-Max scaling
        scaledValue = (value - dataMin) / range_val
        scaledRow.append(scaledValue)
    return scaledRow