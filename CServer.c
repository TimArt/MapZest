#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <libpq-fe.h>

#define PORT 6861
#define ADDRESS "172.22.1.234"

PGconn *conn;

char* signIn(char* signInBuffer, int n){
  char currChar = '0';
  int counter = 0;
  char UserID[n];
  char PassHash[32];
  //Set To Default Error Message
  char* ReturnMessage = (char*)malloc(67);
  do{
    char temp = *(signInBuffer);
    currChar = temp;
    UserID[counter] = currChar;
    counter++;
    signInBuffer++;
  }while(currChar != '0');
  UserID[counter-1] ='\0'; 
  int x;
  int PassCounter = 0;
  for(x = counter; x < n; x++){
    PassHash[PassCounter] = *(signInBuffer);
    signInBuffer++;
    PassCounter++;
  }
  PassHash[PassCounter] = '\0';

  //SQL CALL HERE
  char* queryString = (char*)malloc(n + 40);
  strcat(queryString, "SELECT * FROM get_user_password_hash ('");
  strcat(queryString, UserID);
  strcat(queryString,"');");
  printf("Query:\n%s\n",queryString);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage[0]='0';
    return ReturnMessage;
  }

  ReturnMessage[0]='1';
  PQclear(res);
  char newToken[65];
  for(x = 0; x < 64; x++){
    newToken[x] = (char)(rand() % 10 + 48);
    ReturnMessage[x+1] = newToken[x];
  }
  newToken[64] = '\0';
  ReturnMessage[65] = '[';
  ReturnMessage[66] = '\0';
  char *queryString2 = (char*)malloc(64+100); 
  memset(&queryString2[0], 0, sizeof(queryString2));
  strcat(queryString2, "CALL set_user_auth_token ('");
  strcat(queryString2, UserID);
  strcat(queryString2, "',E'\\\\");
  strcat(queryString2, newToken);
  strcat(queryString2, "');");
  //SQL GETUID->GetLocation
  res = PQexec(conn, queryString2);
  return ReturnMessage;
}

short checkSignInToken(char* token){
  short returnBool = 0;
  //SQL CHECK Token
  char* queryString = (char*)malloc(120);
  memset(&queryString[0], 0, sizeof(queryString));
  strcat(queryString, "SELECT user_id FROM user_auth_tokens WHERE auth_token=E'\\\\");
  strcat(queryString, token);
  strcat(queryString, "';");
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    return 0;
  }
  PQclear(res);
  return 1;
}

char* getMyLocation(char* token1){
  char* ReturnMessage = (char*)malloc(200);
  memset(&ReturnMessage[0], 0, 200);

 char token[65];
  for(int x = 0; x < 64; x++){
    token[x] = *(token1);
    token1++;
  }
  token[64] = '\0';


  if(checkSignInToken(token) == 0){
    ReturnMessage[0]=0;
    return ReturnMessage;
  }
  printf("Bfore query");
  char* queryString = (char*)malloc(300);
  memset(&queryString[0], 0, 300);
  strcat(queryString, "select latitude, longitude from locations where user_id IN (Select user_id from user_auth_tokens where auth_token=E'\\\\");
  strcat(queryString, token);
  strcat(queryString, "');");
  //SQL GETUID->GetLocation

  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage[0]=0;
    return ReturnMessage;
  }
  free(queryString);
  printf("RIGHT BEFORE SETTING RETURNMESSAGE");
  ReturnMessage[0]=1;
  char* lat = PQgetvalue(res,0,0);
  char* lon = PQgetvalue(res,0,1);
  ReturnMessage[1] = *(lat);
  lat++;
  ReturnMessage[2] = *(lat);
  lat++;
  ReturnMessage[3] = *(lat);
  lat++;
  ReturnMessage[4] = *(lat);
  lat++;
  ReturnMessage[5] = *(lon);
  lon++;
  ReturnMessage[6] = *(lon);
  lon++;
ReturnMessage[7] = *(lon);
  lon++;
ReturnMessage[8] = *(lon);
  lon++;
  ReturnMessage[9] = '[';
  ReturnMessage[10] = '\0';
  return ReturnMessage;
}

char updateMyLocation(char* message){
	
  int x;
  char token[65];
  char latitude[5];
  char longitude[5];
  char ReturnMessage = 0;
  for(x = 0; x < 64; x++){
    token[x] = message[x];
  }
  token[64] = '\0';
  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }
char* queryString2 = (char*)malloc(300);	
    memset(&queryString2[0], 0, sizeof(queryString2));

strcat(queryString2, "select email from users where user_id IN (Select user_id from user_auth_tokens where auth_token=E'\\\\");
  strcat(queryString2, token);
  strcat(queryString2, "');");
  //SQL GETUID->GetLocation

  PGresult *res1 = PQexec(conn, queryString2);
  if (PQresultStatus(res1) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res1);
    return ReturnMessage;
  }
  
  char* email = PQgetvalue(res1,0,0);

  for(int x = 0; x < 4; x++){
    latitude[x] = message[x+64];
    longitude[x] = message[x+68];
  }
  latitude[4] = '\0';
  longitude[4] = '\0';

  char* queryString = (char*)malloc(200);
  memset(&queryString[0], 0, sizeof(queryString));


  strcat(queryString, "CALL set_user_active_location('");
  strcat(queryString, email);
  strcat(queryString, "',");
  strcat(queryString, latitude);
  strcat(queryString, ",");
  strcat(queryString, longitude);
  strcat(queryString, ");");
  printf("QUERY FOR UPDATE \n%s\n", queryString);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  ReturnMessage = 1;
  return ReturnMessage;
}

char* findMyFriendLocation(char* message){
 int x;
  char token[65];
    char* ReturnMessage = (char*)malloc(11);
  memset(&ReturnMessage[0], 0, sizeof(ReturnMessage));

  for(x = 0; x < 64; x++){
    token[x] = message[x];
  }
  token[64] = '\0';
  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }
char* queryString2 = (char*)malloc(300);
    memset(&queryString2[0], 0, sizeof(queryString2));

strcat(queryString2, "select email from users where user_id IN (Select user_id from user_auth_tokens where auth_token=E'\\\\");
  strcat(queryString2, token);
  strcat(queryString2, "');");
  //SQL GETUID->GetLocation

  PGresult *res1 = PQexec(conn, queryString2);
  if (PQresultStatus(res1) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
   PQclear(res1);
    return ReturnMessage;
  }
  char* email = PQgetvalue(res1,0,0);


  char UserID[200];
  char currChar;
  message = message+64;
  int counter = 0;
  do{
    char temp = *(message);
    currChar = temp;
    UserID[counter] = currChar;
    counter++;
    message++;
  }while(currChar != '0');

  UserID[counter-1] = '\0';

  char* queryString3 = (char*)malloc(300);
    memset(&queryString3[0], 0, sizeof(queryString3));

strcat(queryString3, "select latitude, longitude from get_user_friends('");
  strcat(queryString3, email);
  strcat(queryString3, "') where email='");
  strcat(queryString3, UserID);
  strcat(queryString3,"' Limit 1;");
  //SQL GETUID->GetLocation
  PGresult *res2 = PQexec(conn, queryString3);
  if (PQresultStatus(res2) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
   PQclear(res2);
    return ReturnMessage;
  }
  if(PQntuples(res2) < 1){
    return ReturnMessage;
  }


  ReturnMessage[0]=1;
  char* lat = PQgetvalue(res2,0,0);
  char* lon = PQgetvalue(res2,0,1);
  ReturnMessage[1] = *(lat);
  lat++;
  ReturnMessage[2] = *(lat);
  lat++;
  ReturnMessage[3] = *(lat);
  lat++;
  ReturnMessage[4] = *(lat);
  lat++;
  ReturnMessage[5] = *(lon);
  lon++;
  ReturnMessage[6] = *(lon);
  lon++;
ReturnMessage[7] = *(lon);
  lon++;
ReturnMessage[8] = *(lon);
  lon++;
  ReturnMessage[9] = '[';
  ReturnMessage[10] = '\0';

  return ReturnMessage;

}

int connectToDatabase(){
  conn = PQconnectdb("user=greg password=thisismypassword dbname=mapzest");
  if(PQstatus(conn) == CONNECTION_BAD){
    printf("Can't connect to DB");
    return 1;
  }
  return 0;
}


int main(){
  int dbstatus;
  dbstatus = connectToDatabase();
  if(dbstatus == 1){
    return 1;
  }


    int sockfd;
    struct sockaddr_in serverAddr;

    int newSocket;
    struct sockaddr_in newAddr;

    socklen_t addr_size;

    sockfd=socket(PF_INET, SOCK_STREAM, 0);
    memset(&serverAddr, '\0', sizeof(serverAddr));

    serverAddr.sin_family=AF_INET;
    serverAddr.sin_port=htons(PORT);
    serverAddr.sin_addr.s_addr=inet_addr(ADDRESS);

    bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
    listen(sockfd, 5);
    addr_size = sizeof(newAddr);
while(1){
    newSocket=accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);
    //strcpy(buffer, "HELLO");
    //Recieve Message MAKE SURE IN JAVA TO PUT A CHAR AT THE BEGINNING
  while(1){
    char * buffer  = (char*)malloc(sizeof(char)*2048);
memset(&buffer[0], 0, sizeof(buffer));
    int n = read(newSocket, buffer, 2048);
    char *message = buffer+1;
    char testChar = *(buffer);
    if(testChar == '0'){
      strcpy(buffer, signIn(message, n));
      //buffer = signIn(message);
      int writetemp = write(newSocket, buffer, strlen(buffer)*sizeof(char));
    }else if(testChar == '1'){
      char* justToken = buffer+1;
      strcpy(buffer, getMyLocation(justToken));
      //buffer = getMyLocation(justToken);
      write(newSocket, buffer, sizeof(char)*strlen(buffer));
    }else if(testChar == '2'){
      buffer[0] = updateMyLocation(message);
      buffer[1] = '[';
      //buffer = updateMyLocation(message);
      send(newSocket, buffer, strlen(buffer), 0);
    }else if(testChar == '3'){
	    printf("3 thing%s\n", buffer);
      strcpy(buffer, findMyFriendLocation(message));
      //buffer = findMyFriendLocation(message);
      send(newSocket, buffer, strlen(buffer), 0);
    }else{
      printf("NOTHIN MATCHED");
      break;
    }
    free(buffer);
  }
}
  return 0;
}
