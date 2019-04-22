from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException 
from tencentcloud.monitor.v20180724 import monitor_client, models 
import json
from prometheus_client import CollectorRegistry, push_to_gateway, Gauge, write_to_textfile

def get_monitor_data(metric,InstanceValue):
     try: 
         cred = credential.Credential("", "") 
         httpProfile = HttpProfile()
         httpProfile.endpoint = "monitor.tencentcloudapi.com"
     
         clientProfile = ClientProfile()
         clientProfile.httpProfile = httpProfile
         client = monitor_client.MonitorClient(cred, "ap-beijing", clientProfile) 
     
         req = models.GetMonitorDataRequest()
         params = '''{"Namespace":"QCE/CDB","MetricName":"%s","Period":300,"Instances":[{"Dimensions":[{"Name":"InstanceId","Value":"%s"}]}]}'''%(metric,InstanceValue)
         req.from_json_string(params)
     
         resp = client.GetMonitorData(req) 
         return json.loads(resp.to_json_string())
     
     except TencentCloudSDKException as err: 
         print(err) 
def push_data_prom():
    '''
    #https://cloud.tencent.com/document/api/248/30386
    '''
    Metrics = ['QPS','TPS','CPUUseRate','VolumeRate','ThreadsConnected','SlowQueries']
    InstanceValue= ['cdb-mf79cwrs','cdb-nr0r1jvu','cdb-g79uoi3m','cdbro-2hnt1w2y','cdb-n6udr136','cdb-i9nxikys','cdb-lbwti8n6','cdb-93ezj3hi','cdb-7kfrnqja','cdb-hvolsxxa']
    registry = CollectorRegistry()
    g = Gauge('tecent_cdb_endpoint', 'cdb', ['info','metric','instanceid'], registry=registry)
    for i in InstanceValue:
       for m in Metrics:
           result = get_monitor_data(m,i)
           instanceid = result['DataPoints'][0]['Dimensions'][0]['Value']
           value =  result['DataPoints'][0]['Values'][-1]
           print instanceid,m,value
           g.labels('tecent-cdb',m,instanceid).set(value)
    push_to_gateway('pushgateway:9091', job='tecent-cdb', registry=registry)


push_data_prom()
