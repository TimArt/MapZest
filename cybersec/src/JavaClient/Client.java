package JavaClient;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ConnectException;
import java.net.Socket;
import java.net.UnknownHostException;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.security.MessageDigest;
import java.util.Arrays;
import java.util.Scanner;

public class Client {

    public static void main(String[] args) throws Exception { 
        Scanner in = new Scanner(System.in);
        Socket s;
        try {
            // Set up connection and (de)framer
            s = new Socket("172.22.1.234", 6861);
        } catch (UnknownHostException e) {
            System.err.println("Error Connecting To Server");
            return;
        } catch (IllegalArgumentException iae) {
            System.err.println("IllegalArgumentException Thrown\n" + iae.getStackTrace());
            return;
        } catch (ConnectException ce) {
            System.err.println("ConnectionException Thrown\n" + ce.getStackTrace());
            return;
        }
        OutputStream ScannerOut = s.getOutputStream();
        InputStream ScannerIn = s.getInputStream();
        char input = 's';
        String token = null;
        do {
            switch (input) {
            case 's':
                System.out.print("LOGIN\nUsername: ");
                String username = in.nextLine();
                System.out.print("Password: ");
                String password = in.nextLine();
                byte[] message = new byte[username.length() + password.length() + 3];
                message[0] = '0';
                byte[] userBytes = username.getBytes();
                for(int x = 1; x < username.length()+1; x++) {
                    message[x] = userBytes[x-1];
                }
                message[username.length()+1] = '0';
                int counter = 0;
                for(int x = username.length()+2; x < message.length-1; x++) {
                    message[x] = password.getBytes()[counter];
		    counter++;
                }
		message[username.length() + password.length() + 2] = '\0';
                ScannerOut.write(message);
                break;
            case 'u':
                System.out.print("UPDATE\nLatitude: ");
                Float lat = in.nextFloat();
		String latitude = String.valueOf(lat).substring(0,4);
                System.out.print("\nLongitude: ");
		Float lon = in.nextFloat();
                String longitude = String.valueOf(lat).substring(0,4);
                byte[] updateMessage = new byte[72];
                updateMessage[0] = '2';
                byte[] tokenBytes = token.getBytes();
                for(int x = 1; x < 65; x++) {
                    updateMessage[x] = tokenBytes[x-1];
                }
                int updateCounter = 0;
		byte[] latbytes = latitude.getBytes();
                for(int x = 65; x < 69; x++) {
                    updateMessage[x] = latbytes[updateCounter];
                    updateCounter++;
                }
                byte[] longbytes = longitude.getBytes();
                updateCounter = 0;
                for(int x = 69; x < 72; x++) {
                    updateMessage[x] = longbytes[updateCounter];
                    updateCounter++;
                }
                ScannerOut.write(updateMessage);
                break;
            case 'g':
                System.out.println("Getting your location ");
                byte[] getMessage = new byte[token.getBytes().length +2];
		byte[] tokenBytes1 = token.getBytes();
		getMessage[0] = '1';
                for(int x = 1; x < 65; x++) {
                    getMessage[x] = tokenBytes1[x-1];
                }
		getMessage[token.getBytes().length+1] = '\0';
                ScannerOut.write(getMessage);
                break;
            case 'f':
                System.out.println("Getting Friend's Location");
                System.out.print("Friend's Username: ");
                String friendu = in.nextLine();
                byte[] friendMessage = new byte[67 + friendu.length()];
                friendMessage[0] = '3';
                byte[] tokenBytes2 = token.getBytes();
                for(int x = 1; x < 65; x++) {
                    friendMessage[x] = tokenBytes2[x-1];
                }
                byte[] friendbytes = friendu.getBytes();
                for(int x = 65; x < friendMessage.length-2; x++) {
                    friendMessage[x] = friendbytes[x-65];
                }
                friendMessage[65 + friendu.length()] = '0';
		friendMessage[66 + friendu.length()] = '\0';
		ScannerOut.write(friendMessage);
		
                break;
            default:
                System.err.println("Bad User Input");
            }
	    int c;
	    byte[] b = {0};
	    boolean notFound = true;
	    ByteArrayOutputStream output = new ByteArrayOutputStream();
	    while(notFound && (c = ScannerIn.read(b)) != -1){
		output.write(b);
		char bleh = (char)b[0];
		if(bleh == '['){
		   notFound = false;
		}
	    }
            byte[] response = output.toByteArray();
            if(response[0] == 0) {
                System.err.println("Error With Data You Sent");
            }else {
                switch (input) {
                case 's':
                    System.out.println("Successful Login");
                    byte[] tok = Arrays.copyOfRange(response, 1, response.length);
		    token = "";
		    for(int x = 0; x < tok.length; x++){
			token += Character.getNumericValue(tok[x]);
		    }
                    input = getInput();
                    break;
                case 'u':
                    System.out.println("System Updated");
                    input = getInput();
                    break;
                case 'g':
                    byte[] lat = Arrays.copyOfRange(response, 1, 5);
                    byte[] lon = Arrays.copyOfRange(response, 5, 9);
                    System.out.print("Latitude: ");
		    for(int x = 0; x < 4; x++){
			    if(lat[x] == '.'){
				    System.out.print(".");
			    }else{
			System.out.print(Character.getNumericValue(lat[x]));
			    }
		    }
		    System.out.print("\nLongitude: ");

		    for(int x = 0; x < 4; x++){
			    if(lat[x] == '.'){
				    System.out.print(".");
			    }else{
                        System.out.print(Character.getNumericValue(lon[x]));
			    }
                    }
		    System.out.println("");
                    input = getInput();
                    break;
                case 'f':
                    byte[] lat2 = Arrays.copyOfRange(response, 1, 5);
                    byte[] lon2 = Arrays.copyOfRange(response, 5, 9);
                    System.out.print("Latitude: ");
                    for(int x = 0; x < 4; x++){
			    if(lat2[x] == '.'){
				    System.out.print(".");
			    }else{
                        System.out.print(Character.getNumericValue(lat2[x]));
			    }
                    }
                    System.out.print("\nLongitude: ");

                    for(int x = 0; x < 4; x++){
			    if(lon2[x] == '.'){
				    System.out.print(".");
			    }else{
                        System.out.print(Character.getNumericValue(lon2[x]));
			    }
                    }
                    System.out.println("");
		    input = getInput();
		    break;
                default:
                    input = getInput();
                }
            }
        }while(input != 'q');
    }
    
    public static char getInput() {
        System.out.println("What Would You Like To Do?");
        System.out.println("Type u For Updating Your Location");
        System.out.println("Type g For Getting Your Location");
        System.out.println("Type f For Getting a Friend's location");
        System.out.println("Type q To Quit");
        Scanner in = new Scanner(System.in);
        String input = in.nextLine();
        return input.charAt(0);
    }
}
