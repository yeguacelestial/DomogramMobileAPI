#include <DHT.h>

// Leds
const int led1 = 2;
const int led2 = 3;
const int led3 = 4;
const int led4 = 5;
const int led5 = 6;
const int led6 = 7;

// Sensor de temperatura y humedad
#define pinDHT A0
#define DHTtype DHT11
DHT dht(pinDHT, DHTtype);

// Sensor de distancia
const int EchoPin = 10;
const int TriggerPin = 11;
float distancia;
long tiempo;

void setup()
{
    // Inicializar monitor serial
    Serial.begin(115200);

    // Leds
    pinMode(led1, OUTPUT);
    pinMode(led2, OUTPUT);
    pinMode(led3, OUTPUT);
    pinMode(led4, OUTPUT);
    pinMode(led5, OUTPUT);
    pinMode(led6, OUTPUT);

    // Sensor de temperatura y humedad
    dht.begin();

    // Sensor ultrasonico
    pinMode(TriggerPin, OUTPUT);
    pinMode(EchoPin, INPUT);
}

void loop()
{
    // LEDS
    // test_leds();

    // Sensor de temperatura y humedad
    // test_dht();

    // Sensor ultrasonico
    // test_ultrasonico();

    // TODO - Servomotores
}

// Leds
int test_leds()
{
    for (int x = 2; x <= 7; x++)
    {
        digitalWrite(x, HIGH);
        delay(1000);
        digitalWrite(x, LOW);
    }
}

// Sensor de temperatura y humedad
int test_dht()
{
    Serial.println(dht.readTemperature() + String("°C"));
    Serial.println(dht.readHumidity() + String("%"));
    delay(1000);
}

// Sensor ultrasonico
int test_ultrasonico()
{
    int cm = ping(TriggerPin, EchoPin);
    Serial.println(String("DISTANCIA => ") + cm + String("cm"));
    delay(1000);
}

int ping(int TriggerPin, int EchoPin)
{
    long duration, distanceCm;

    digitalWrite(TriggerPin, LOW); // Generar pulso limpio
    delayMicroseconds(4);
    digitalWrite(TriggerPin, HIGH); // generar trigger de 10us
    delayMicroseconds(10);
    digitalWrite(TriggerPin, LOW);

    duration = pulseIn(EchoPin, HIGH); // Medir tiempo entre pulsos, en microsegundos

    distanceCm = duration * 10 / 292 / 2; // Convertir distancia en cm
    return distanceCm;
}