import xml.etree.ElementTree as ElementTree
from flask import Flask, request, Response
import requests
from waitress import serve

app = Flask(__name__)
# WMS linkleri
target_wms_url = "http://subdomain.targetdomain.com/ows"
source_wms_url = "http://my.domain.com/wms/mywms"
ElementTree.register_namespace("", "http://www.opengis.net/wms")
ElementTree.register_namespace("xlink", "http://www.w3.org/1999/xlink")


@app.route("/wms-proxy", methods=["GET"])
def proxy_wms_request():
    try:
        query_string = request.query_string.decode(
            "utf-8"
        )  # Request parameters
        target_url = f"{target_wms_url}?{query_string}"
        response = requests.get(target_url)  # Sending a request to the target wms url

        if response.headers.get('Content-Type') == 'text/xml':
            # Links in the response are replaced using ElementTree library
            root = ElementTree.fromstring(response.content)

            xlink_elements = root.findall(
                ".//{*}OnlineResource"
            )  # Links are in <OnlineResources /> element
            for online_resource in xlink_elements:
                old_href = online_resource.get("{http://www.w3.org/1999/xlink}href")
                new_href = old_href.replace(target_wms_url, source_wms_url)
                # Modify the xlink:href attribute
                online_resource.set("{http://www.w3.org/1999/xlink}href", new_href)

            # Preparing the modified response
            modified_response = ElementTree.tostring(root, encoding="utf-8").decode("utf-8")

            return Response(
                modified_response, content_type=response.headers["Content-Type"]
            )
        else:
            return response.content, response.status_code, {'Content-Type': response.headers.get('Content-Type')}

    except Exception as e:
        # Send an error message if there is an exception
        error_message = f"Error: {str(e)}"
        return error_message, 500


if __name__ == "__main__":
    serve(app, host="127.0.0.1", port=14520)
else:
    serve(app, host="127.0.0.1", port=14520)
