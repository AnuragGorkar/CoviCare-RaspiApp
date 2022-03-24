import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.PBEKeySpec;
import javax.crypto.spec.SecretKeySpec;

import java.security.NoSuchAlgorithmException;
import java.nio.charset.StandardCharsets;

import java.security.spec.InvalidKeySpecException;
import java.security.spec.KeySpec;
import java.util.HashMap;
import java.util.Map;

import java.util.HashMap;
import java.util.Map;

import java.util.Base64;

class EncryptVitals{	
	private static final String UNICODE_FORMAT = "UTF-8";

    private final static String HEX = "0123456789ABCDEF";
    
    public String encryptDataForVitalsStream(String dataToEncrypt, SecretKey key){
	
	try {
		
			Cipher cipher = Cipher.getInstance("AES");
			
            byte[] text = dataToEncrypt.getBytes(UNICODE_FORMAT);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] textEncrypted = cipher.doFinal(text);
	    
	    String data = toHex(textEncrypted);
	
            Map<String, Object> returnMap = new HashMap<String, Object>();
            returnMap.put("Data", data);
            
            return returnMap.toString();
            
        } catch (Exception e) {
	    return "Error";
        }
	
	
	
    }
	
    public static void main(String[] args) {
        EncryptVitals encryptVitals =  new EncryptVitals();
        encryptVitals.EncryptVitalsData(args[0], args[1], args[2]);  
	
	//System.out.println(String.valueOf(encryptVitals.toByte("4259852FC118A92E6ECE45D1D272DE8DCB6FECFB8AFA030EA3AB32C79F405C4A6979BD02D665C90B0780DE804933D7AA2FCD0A0F1C434C2757560E5AD28BF157")));
    }
    
    public void EncryptVitalsData(String dataToEncrypt, String password, String salt){
	
		try {
			SecretKey key = getKeyFromPassword(password, salt);
		
			Cipher cipher = Cipher.getInstance("AES");
			
            byte[] text = dataToEncrypt.getBytes(UNICODE_FORMAT);
            cipher.init(Cipher.ENCRYPT_MODE, key);
            byte[] textEncrypted = cipher.doFinal(text);
	    
	    String data = toHex(textEncrypted);
	
            Map<String, Object> returnMap = new HashMap<String, Object>();
            returnMap.put("Password", password);
            returnMap.put("Salt", salt);
            returnMap.put("Data", data);
            
            System.out.println(returnMap.toString());
            
        } catch (Exception e) {
        }
		
		
	}
	
	private static void appendHex(StringBuffer sb, byte b) {
        sb.append(HEX.charAt((b >> 4) & 0x0f)).append(HEX.charAt(b & 0x0f));
    }
	
	public static String toHex(byte[] buf) {
        if (buf == null)
            return "";
        StringBuffer result = new StringBuffer(2 * buf.length);
        for (int i = 0; i < buf.length; i++) {
            appendHex(result, buf[i]);
        }
        return result.toString();
    }

	public static SecretKey getKeyFromPassword(String password, String salt)
            throws NoSuchAlgorithmException, InvalidKeySpecException {
        SecretKeyFactory factory = SecretKeyFactory.getInstance("PBKDF2WithHmacSHA256");
        KeySpec spec = new PBEKeySpec(password.toCharArray(), salt.getBytes(), 64, 256);
        SecretKey originalKey = new SecretKeySpec(factory.generateSecret(spec).getEncoded(), "AES");
        return originalKey;
    }
	
	public static byte[] toByte(String hexString) {
        int len = hexString.length() / 2;
        byte[] result = new byte[len];
        for (int i = 0; i < len; i++)
            result[i] = Integer.valueOf(hexString.substring(2 * i, 2 * i + 2),
                    16).byteValue();
        return result;
    }
}
