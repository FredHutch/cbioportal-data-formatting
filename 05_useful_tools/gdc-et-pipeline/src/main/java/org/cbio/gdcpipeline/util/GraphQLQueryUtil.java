package org.cbio.gdcpipeline.util;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.OutputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.List;
import java.util.zip.GZIPInputStream;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.json.simple.parser.JSONParser;
import org.json.simple.parser.ParseException;

/**
 *
 * @author heinsz
 */
public class GraphQLQueryUtil {


    private static Log LOG = LogFactory.getLog(GraphQLQueryUtil.class);

    private static HttpURLConnection getConnectionForGDCGrapql(int length, String endpoint) throws IOException {
        URL url = new URL(endpoint);
        HttpURLConnection con = (HttpURLConnection) url.openConnection();
        con.setRequestMethod("POST");
        con.setRequestProperty("Content-Type", "application/json");
        con.setRequestProperty("Accept", "application/json");
        con.setRequestProperty("Connection", "keep-alive");
        con.setRequestProperty("DNT", "1");
        con.setRequestProperty("Origin", "file://");
        con.setRequestProperty("Accept-Encoding", "gzip");
        con.setDoOutput(true);
        con.setFixedLengthStreamingMode(length);
        return con;
    }

    private static String createQuery(String query, String datatype, String field, List<String> values) {
        JSONObject queryJson = new JSONObject();
        JSONObject variables = createQueryFilter(datatype, field, values);
        queryJson.put("query", query);
        queryJson.put("variables", variables);
        return queryJson.toJSONString();
    }

    public static JSONObject createQueryFilter(String datatype, String field, List<String> values) {
        JSONObject contentJson = new JSONObject();
        contentJson.put("field", datatype +  "." + field);
        JSONArray jsonValues = new JSONArray();
        jsonValues.addAll(values);
        contentJson.put("value", jsonValues);
        JSONObject filtersJson= new JSONObject();
        filtersJson.put("op", "in");
        filtersJson.put("content", contentJson);
        JSONObject queryVariableJson = new JSONObject();
        queryVariableJson.put("filters", filtersJson);

        return queryVariableJson;
    }

    public static JSONObject query(String endpoint, String query, String datatype, String field, List<String> values) throws IOException {
        query = createQuery(query, datatype, field, values);
        byte[] out = query.getBytes();
        JSONObject jsonResponse = null;
        HttpURLConnection con = GraphQLQueryUtil.getConnectionForGDCGrapql(out.length, endpoint);

        con.connect();
        OutputStream os = con.getOutputStream();
        os.write(out);
        BufferedReader in = new BufferedReader(new InputStreamReader(new GZIPInputStream(con.getInputStream())));

        String responseLine;
        String response = "";
        while((responseLine = in.readLine()) != null) {
            response = response + responseLine;
        }

        in.close();

        JSONParser parser = new JSONParser();
        try {
            jsonResponse = (JSONObject) parser.parse(response);
            LOG.info("Finished calling gdc graphql");
        }
        catch (ParseException e) {
            LOG.error("Could not parse json response.");
        }

        return jsonResponse;
    }

    public static JSONArray getQueryList(JSONObject response, String field) {
        JSONObject data = (JSONObject) response.get("data");
        JSONObject viewer = (JSONObject) data.get("viewer");
        JSONObject repository = (JSONObject) viewer.get("repository");
        JSONObject files = (JSONObject) repository.get(field);
        JSONObject hits = (JSONObject) files.get("hits");
        JSONArray edges = (JSONArray) hits.get("edges");
        return edges;
    }
}
