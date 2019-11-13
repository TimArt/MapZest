#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <libpq-fe.h>

#define PORT 6861
#define ADDRESS "127.0.0.1"

PGconn *conn;

char* signIn(char* signInBuffer){
  char currChar = '\0';
  int counter = 0;
  char UserID[sizeof(signInBuffer)];
  char PassHash[32];
  //Set To Default Error Message
  char* ReturnMessage = malloc(65);
  do{
    currChar = signInBuffer[counter];
    UserID[counter] = currChar;
    counter++;
    if(sizeof(signInBuffer)-counter < 32){
      return ReturnMessage;
    }
  }while(currChar != '\0');

  int x;
  int PassCounter = 0;
  for(x = counter; x < sizeof(signInBuffer); x++){
    if(PassCounter ==32){
      return ReturnMessage;
    }
    PassHash[PassCounter] = signInBuffer[x];
    PassCounter++;
  }

  //SQL CALL HERE
  char* queryString = concat("SELECT UID FROM Users WHERE email=", UserID);
  strcat(queryString,", passhash =");
  strcat(queryString, PassHash)
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage[0]=0;
    return ReturnMessage;
  }

  ReturnMessage[0]=1;
  char* userID = PQgetvalue(res, 0, 0));
  PQclear(res);
  char newToken[64];
  for(x = 0; x < 64; x++){
    newToken[x] = (char)(rand() % 10);
  }

  char* queryString = concat("UPDATE Tokens SET Timestamp = ", timestamp);
  strcat(queryString, ", expires = ");
  strcat(queryString, expiretime);
  strcat(queryString, ", tokenCode = ");
  strcat(queryString, newToken);
  strcat(queryString, "WHERE UID = ");
  strcat(queryString, userID);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage = 0;
    return ReturnMessage;
  }

  return ReturnMessage;
}

short checkSignInToken(char* token){
  short returnBool = 0;

  //SQL CHECK Token
  char* queryString = concat("SELECT * FROM Users WHERE token=", token);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    return 0;
  }
  returnBool = PQntuples(const PGresult *res);
  PQclear(res);
  return returnBool;
}

char* getMyLocation(char* token){

  char* ReturnMessage = malloc(9);

  if(checkSignInToken(token) == 0){
    ReturnMessage[0]=0;
    return ReturnMessage;
  }

  char* queryString = concat("SELECT latitude, longitude FROM Users WHERE token=", token);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage[0]=0;
    return ReturnMessage;
  }

  ReturnMessage[0]=1;
  strcat(ReturnMessage, PQgetvalue(res, 0, 0));
  strcat(ReturnMessage, PQgetvalue(res, 0, 1));
  PQclear(res);
  return ReturnMessage;
}

char updateMyLocation(char* message){
  int x;
  char token[64];
  char latitude[4];
  char longitude[4];
  char ReturnMessage = 0;
  for(x = 0; x < 64; x++){
    token[x] = message[x];
  }
  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }
  for(x = 0; x < 4; x++){
    latitude[x] = message[x+64];
    longitude[x] = message[x+68];
  }

  char* queryString = concat("UPDATE Users SET latitude = ", latitude);
  strcat(queryString, ", longitude = ");
  strcat(queryString, longitude);
  strcat(queryString, "WHERE token = ");
  strcat(queryString, token);
  //SQL GETUID->GetLocation
  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage = 0;
    return ReturnMessage;
  }

  ReturnMessage =1;
  PQclear(res);
  return ReturnMessage;
}

char* findMyFriendLocation(char* message){
  int x;
  char token[64];
  char* ReturnMessage = malloc(9);
  for(x = 0; x < 64; x++){
    token[x] = message[x];
  }

  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }

  char currChar = '\0';
  int counter = 0;
  char UserID[sizeof(message)];
  do{
    currChar = message[counter];
    UserID[counter] = currChar;
    counter++;
  }while(currChar != '\0');

  //SQL Get location from UID
  char* queryString = concat("SELECT latitude, longitude FROM Users WHERE Friend=", friend);

  PGresult *res = PQexec(conn, queryString);
  if (PQresultStatus(res) != PGRES_TUPLES_OK) {
    printf("No data retrieved\n");
    PQclear(res);
    ReturnMessage[0]=0;
    return ReturnMessage;
  }

  ReturnMessage[0]=1;
  strcat(ReturnMessage, PQgetvalue(res, 0, 0));
  strcat(ReturnMessage, PQgetvalue(res, 0, 1));
  PQclear(res);
  return ReturnMessage;
  return ReturnMessage;
}

int connectToDatabase(){
  conn = PQconnectdb("user=group1 password=thisisapassword dbname=projectdatabase");
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
    char buffer[1024];

    sockfd=socket(PF_INET, SOCK_STREAM, 0);
    memset(&serverAddr, '\0', sizeof(serverAddr));

    serverAddr.sin_family=AF_INET;
    serverAddr.sin_port=htons(PORT);
    serverAddr.sin_addr.s_addr=inet_addr(ADDRESS);

    bind(sockfd, (struct sockaddr*)&serverAddr, sizeof(serverAddr));
  while(1){
    listen(sockfd, 5);
    addr_size = sizeof(newAddr);

    newSocket=accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);

    //strcpy(buffer, "HELLO");

    //Recieve Message MAKE SURE IN JAVA TO PUT A CHAR AT THE BEGINNING
    recv(newSocket, buffer, 1024, 0);
    char* message = malloc(1023);
    int tempx;
    for(tempx = 0; tempx < sizeof(buffer)-1; tempx++){
      message[tempx] = buffer[1+tempx];
    }
    if(buffer[0] == 0){
      strcpy(buffer, signIn(message));
      //buffer = signIn(message);
      send(newSocket, buffer, strlen(buffer), 0);
    }else if(buffer[0] == 1){
      char* justToken = malloc(64);
      for(tempx = 0; tempx < 64; tempx++){
        justToken[tempx] = buffer[tempx+1];
      }
      strcpy(buffer, getMyLocation(justToken));
      //buffer = getMyLocation(justToken);
      send(newSocket, buffer, strlen(buffer), 0);
      free(justToken);
    }else if(buffer[0] == 2){
      buffer[0] = updateMyLocation(message);
      //buffer = updateMyLocation(message);
      send(newSocket, buffer, strlen(buffer), 0);
    }else if(buffer[0] == 3){
      strcpy(buffer, findMyFriendLocation(message));
      //buffer = findMyFriendLocation(message);
      send(newSocket, buffer, strlen(buffer), 0);
    }else{
      buffer[0] = 0;
      send(newSocket, buffer, strlen(buffer), 0);
    }

    free(message);

  }
  return 0;
}
