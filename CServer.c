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

//PGconn *conn;

char* signIn(char* signInBuffer){
  char currChar = '\0';
  int counter = 0;
  char UserID[sizeof(signInBuffer)];
  char PassHash[32];
  //Set To Default Error Message
  char* ReturnMessage;
  memset(ReturnMessage, 0, 65);
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



  return ReturnMessage;
}

short checkSignInToken(char* token){
  short returnBool = 0;
  char tokenString[64];
  int x = 0;
  for(x = 0; x < 64; x++){
    tokenString[x] = token[x];
  }
  //SQL CHECK Token

  return returnBool;
}

char* getMyLocation(char* token){

  char* ReturnMessage;
  memset(ReturnMessage, 0, 9);

  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }
  //SQL GETUID->GetLocation
  return ReturnMessage;
}

char setMyLocation(char* message){
  int x;
  char token[64];
  char ReturnMessage = 0;
  for(x = 0; x < 64; x++){
    token[x] = message[x];
  }
  if(checkSignInToken(token) == 0){
    return ReturnMessage;
  }

  //SQL Update Location
  return ReturnMessage;
}

char* findMyFriendLocation(char* message){
  int x;
  char token[64];
  char* ReturnMessage;
  memset(ReturnMessage, 0, 9);
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
    if(sizeof(message)-counter < 32){
      return ReturnMessage;
    }
  }while(currChar != '\0');

  //SQL Get location from UID

  return ReturnMessage;
}

int connectToDatabase(){
  PGconn *conn = PQconnectdb("user=<USERNAME> password=<PASSWORD> dbname=<DATABASENAME");
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
  while(1){

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

    listen(sockfd, 5);
    addr_size = sizeof(newAddr);

    newSocket=accept(sockfd, (struct sockaddr*)&newAddr, &addr_size);

    strcpy(buffer, "HELLO");

    //Recieve Message
    //recv(newSocket, buffer, 1024, 0);
    send(newSocket, buffer, strlen(buffer), 0);

  }
  return 0;
}
