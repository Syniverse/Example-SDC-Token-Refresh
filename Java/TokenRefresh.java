import com.sun.jersey.api.client.Client;
import com.sun.jersey.api.client.ClientResponse;
import com.sun.jersey.api.client.WebResource;

import javax.ws.rs.core.MediaType;

import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

public class TokenRefresh {

	private static final String URI = "https://beta-api.syniverse.com/saop-rest-data/v1/apptoken-refresh";
	
	/* 
	 * Parameters:
	 * consumerKey, consumerSecret, old token, validity period
	 */
	public static void main(String[] args) {
		TokenRefresh tr = new TokenRefresh();
		RefreshRequest request = new RefreshRequest(args[0], args[1], args[2], Integer.parseInt(args[3]));
		RefreshResponse response;
		try {
			response = tr.refresh(request);
			System.out.println("The new token is "+response.newToken+", which is valid for "+response.validityTime);
		} catch (Exception e) {
			e.printStackTrace();
		}
	}

	public RefreshResponse refresh(RefreshRequest request) throws Exception {
		Client client = Client.create();
	    WebResource webResource = client.resource(URI);
	    ClientResponse clientResponse = webResource
	    		.queryParam("consumerkey", request.consumerKey)
	    		.queryParam("consumersecret", request.consumerSecret)
	    		.queryParam("oldtoken", request.oldToken)
	    		.queryParam("validity", Long.toString(request.validityTime))
	    		.accept(MediaType.APPLICATION_JSON_TYPE)
	    		.get(ClientResponse.class);
		if (clientResponse.getStatus() != 200) {
			System.out.println(clientResponse.getEntity(String.class));
			throw new Exception("Refresh request got " + clientResponse.getStatus());
		}
		RefreshResponse response = new RefreshResponse();
		// parse the returned JSON
		try {
			String responseStr = clientResponse.getEntity(String.class);
			JSONParser parser = new JSONParser();
			JSONObject obj = (JSONObject)parser.parse(responseStr);
			response.newToken = (String) obj.get("accessToken");
			response.validityTime = (Long) obj.get("validityTime");

		}catch (ParseException pe) {
			pe.printStackTrace();
			throw new Exception("Request failed");
		} finally {		
			client.destroy();
		}
		return response;
	}

	private static class RefreshRequest {		
		public final String consumerKey;
		public final String consumerSecret;
		public final String oldToken;
		public final long validityTime;

		public RefreshRequest(String consumerKey, String consumerSecret, String oldToken, int validityTime) {
			this.consumerKey = consumerKey;
			this.consumerSecret = consumerSecret;
			this.oldToken = oldToken;
			this.validityTime = validityTime;
		}		
	}
	
	private static class RefreshResponse {
		public String newToken;
		public long validityTime;
		
		public RefreshResponse() {}
	}
}
