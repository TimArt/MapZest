package JavaClient;

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
            s = TLSFactory.getClientSocket("172.22.1.1", 6861);
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
                System.out.print("\nPassword: ");
                String password = in.nextLine();
                MessageDigest digest = MessageDigest.getInstance("SHA-256");
                byte[] encodedhash = digest.digest(
                  password.getBytes(StandardCharsets.US_ASCII));
                byte[] message = new byte[username.length() + 66];
                message[0] = 0;
                byte[] userBytes = username.getBytes();
                for(int x = 1; x < username.length()+1; x++) {
                    message[x] = userBytes[x-1];
                }
                message[username.length()+1] = '\0';
                int counter = 0;
                for(int x = username.length()+2; x < message.length; x++) {
                    message[x] = encodedhash[counter];
                }
                ScannerOut.write(message);
                break;
            case 'u':
                System.out.print("UPDATE\nLatitude: ");
                Float latitude = in.nextFloat();
                System.out.print("\nLongitude: ");
                Float longitude = in.nextFloat();
                byte[] updateMessage = new byte[72];
                updateMessage[0] = 2;
                byte[] tokenBytes = token.getBytes();
                for(int x = 1; x < 65; x++) {
                    updateMessage[x] = tokenBytes[x-1];
                }
                byte[] latbytes = latitude.toHexString(latitude).getBytes();
                int updateCounter = 0;
                for(int x = 65; x < 69; x++) {
                    updateMessage[x] = latbytes[updateCounter];
                    updateCounter++;
                }
                byte[] longbytes = longitude.toHexString(longitude).getBytes();
                updateCounter = 0;
                for(int x = 69; x < 72; x++) {
                    updateMessage[x] = latbytes[updateCounter];
                    updateCounter++;
                }
                ScannerOut.write(updateMessage);
                break;
            case 'g':
                System.out.println("Getting your location ");
                byte[] getMessage = new byte[65];
                getMessage[0] = 1;
                byte[] tokenBytes1 = token.getBytes();
                for(int x = 1; x < 65; x++) {
                    getMessage[x] = tokenBytes1[x-1];
                }
                ScannerOut.write(getMessage);
                break;
            case 'f':
                System.out.println("Getting Friend's Username");
                System.out.print("Friend's Username: ");
                String friendu = in.nextLine();
                byte[] friendMessage = new byte[66 + friendu.length()];
                friendMessage[0] = 1;
                byte[] tokenBytes2 = token.getBytes();
                for(int x = 1; x < 65; x++) {
                    friendMessage[x] = tokenBytes2[x-1];
                }
                byte[] friendbytes = friendu.getBytes();
                for(int x = 65; x < friendMessage.length-1; x++) {
                    friendMessage[x] = friendbytes[x-1];
                }
                friendMessage[65 + friendu.length()] = '\0';
                ScannerOut.write(friendMessage);
                break;
            default:
                System.err.println("Bad User Input");
            }
            byte[] response = ScannerIn.readAllBytes();
            if(response[0] == 0) {
                System.err.println("Error With Data You Sent");
            }else {
                switch (input) {
                case 's':
                    System.out.println("Successful Login");
                    byte[] tok = Arrays.copyOfRange(response, 1, response.length);
                    token = Arrays.toString(tok);
                    input = getInput();
                    break;
                case 'u':
                    System.out.println("System Updated");
                    input = getInput();
                    break;
                case 'g':
                    byte[] lat = Arrays.copyOfRange(response, 1, 4);
                    ByteBuffer buffer = ByteBuffer.wrap(lat);
                    Float latitude = buffer.getFloat();
                    byte[] lon = Arrays.copyOfRange(response, 5, 8);
                    ByteBuffer buffer2 = ByteBuffer.wrap(lon);
                    Float longitude = buffer2.getFloat();
                    System.out.println("Latitude: " + latitude + "\nLongitude: " + longitude);
                    input = getInput();
                    break;
                case 'f':
                    byte[] lat2 = Arrays.copyOfRange(response, 1, 4);
                    ByteBuffer buffer3 = ByteBuffer.wrap(lat2);
                    Float latitude2 = buffer3.getFloat();
                    byte[] lon2 = Arrays.copyOfRange(response, 5, 8);
                    ByteBuffer buffer4 = ByteBuffer.wrap(lon2);
                    Float longitude2 = buffer4.getFloat();
                    System.out.println("Latitude: " + latitude2 + "\nLongitude: " + longitude2);
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
