#include <DHT.h>
#include <LiquidCrystal.h>

#define DHTPIN 6    // what pin we're connected to
#define DHTTYPE DHT22   // DHT 22  (AM2302)
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);

// Initialize DHT sensor for normal 16mhz Arduino
DHT dht(DHTPIN, DHTTYPE);

void setup() {
        Serial.begin(9600); 
        //Initialize LCD
        lcd.begin(16, 2);
        lcd.print("Temp is");
        //Initialize DHT
        dht.begin();
}

void loop() {
        // Wait a few seconds between measurements.
        delay(2000);
        lcd.setCursor(0, 1);
        // Reading temperature or humidity takes about 250 milliseconds!
        // Sensor readings may also be up to 2 seconds 'old'
        // (its a very slow sensor)
        // Read temperature as Celsius
        float t = dht.readTemperature();
   

        if (isnan(t)) {
                Serial.println("Failed to read from DHT sensor!");
                return;
        }

        Serial.print("Temperature: "); 
        Serial.print(t);
        Serial.print(" *C ");
        lcd.print(t);
        lcd.print(" *C");
}



