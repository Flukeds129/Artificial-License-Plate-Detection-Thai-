#include <ESP8266WiFi.h>
#include <PubSubClient.h>

//your network
const char* ssid = "Wi-Fi NAME";             //ชื่อ Wifi
const char* password = "Wi-Fi Password";     //รหัส Wifi

char *Relay_ON  ;
char *Relay_OFF ;

//การกำหนด MQTT Server
#define MQTTserver "YOUR_MQTT_SERVER"         //กำหนด MQTT Server
#define MQTTport YOUR_MQTT_PORT               //กำหนด MQTT Port
#define MQTTuser "YOUR_MQTT_USERNAME"         //กำหนด MQTT User Name
#define MQTTpassword "YOUR_MQTT_PASSWORD"     //กำหนด MQTT password

WiFiClient WIFI_Client;
PubSubClient client(WIFI_Client);

void setup() {
  pinMode(D0,OUTPUT);     //กำหนดสถานะขา D0 ใช้ในการส่งค่า
  pinMode(D1,OUTPUT);     //กำหนดสถานะขา D1 ใช้ในการส่งค่า
  
  Serial.begin(115200);   //กำหนดค่าความเร็วในการรับ-ส่งข้อมูล         
  Serial.println();
  
      
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);   //Setup WiFi     
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  client.setServer(MQTTserver, MQTTport);  //Setup MQTT Server 
  client.setCallback(callback);
}

void loop() {

  if (!client.connected()) {
    if (client.connect("ESP8266Client", MQTTuser, MQTTpassword)) { //ถ้าเชื่อมต่อ MQTT ได้สำเร็จให้ติดตามหัวข้อที่ชื่อ License Number
      Serial.println("connected");
      client.subscribe("License Number");
    } 
    else {               // แต่ถ้าไม่สำเร็จ ทำการหน่วงเวลา 3 วินาที แล้วลองใหม่่
      Serial.print("failed !");
      Serial.print(client.state());
      Serial.println(" Try again in 3 seconds");
      delay(3000); 
      return;
    }
  }
  client.loop();
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message form topic <");
  Serial.print(topic);
  Serial.print("> : ");
  String message = "";
  int text=0;
  while (text<length) {
    message += (char)payload[text++]; //อ่านข้อความจาก Topic ที่ถูกส่งมา
  }
  
  if (message == "4กง87") {         //ถ้าข้อความที่ได้รับจาก Topic ตรงกับป้ายทะเบียนที่กำหนด
    digitalWrite(D0,0);              //สั่งขา D0 ให้ Relay ON
    digitalWrite(D1,0);              //สั่งขา D1 ให้ Relay ON
    Relay_ON = "Status Relay : ON " ;
    client.publish("License Number",Relay_ON);    //ทำการส่งข้อความสถานะเปิด กลับไปที่ Topic 
  }
  
  else if (message == "USER ON") {   //ถ้าข้อความที่ได้รับจากผู้ใช้เปิด
    digitalWrite(D0,0);              //สั่งขา D0 ให้ Relay ON
    digitalWrite(D1,0);              //สั่งขา D1 ให้ Relay ON
    Relay_ON = "Status Relay : ON " ;
    client.publish("License Number",Relay_ON);    //ทำการส่งข้อความสถานะเปิด กลับไปที่ Topic 
  }
  
  else if (message == "USER OFF"){    //แต่ถ้าได้รับข้อความจากผู้ใช้ให้ปิด 
    digitalWrite(D0,1);               //สั่งขา D0 ให้ Relay OFF
    digitalWrite(D1,1);               //สั่งขา D0 ให้ Relay OFF
    Relay_OFF = "Status Relay : OFF" ;
    client.publish("License Number",Relay_OFF);   //ทำการส่งข้อความสถานะปิด กลับไปที่ Topic 
  }
  
  Serial.println(message);            //แสดงข้อความที่ได้รับจาก Topic
}
