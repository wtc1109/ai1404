--- 模块功能：HTTP功能测试.
-- @author openLuat
-- @module http.testHttp
-- @license MIT
-- @copyright openLuat
-- @release 2018.03.23

module(...,package.seeall)

require"http"
require"socket"
require"lbsLoc"
require"net"
require"utils"
--require"misc"

local _http_received = 0
local function cbFnc(result,prompt,head,body)
    log.info("testHttp.cbFnc",result,prompt)
    if result and head then
        for k,v in pairs(head) do
            log.info("testHttp.cbFnc",k..": "..v)
        end
    end
    if result and body then
        log.info("testHttp.cbFnc","bodyLen="..body:len())
		log.info("testHttp.cbFnc:"..body)
    end
    _http_received = 1
end

local function cbFncFile(result,prompt,head,filePath)
    log.info("testHttp.cbFncFile",result,prompt,filePath)
    if result and head then
        for k,v in pairs(head) do
            log.info("testHttp.cbFncFile",k..": "..v)
        end
    end
    if result and filePath then
        local size = io.fileSize(filePath)
        log.info("testHttp.cbFncFile","fileSize="..size)
        
        --输出文件内容，如果文件太大，一次性读出文件内容可能会造成内存不足，分次读出可以避免此问题
        if size<=4096 then
            log.info("testHttp.cbFncFile",io.readFile(filePath))
        else
			
        end
    end
    --文件使用完之后，如果以后不再用到，需要自行删除
    if filePath then os.remove(filePath) end
end

--[[
local latlng = "reqLbsLoc=0"

function getLocCb(result,lat,lng)
	--log.info("testLbsLoc.getLocCb",result,lat,lng)
	--log.info("result",type(result))
	--log.info("lat",type(lat))
	--log.info("lng",type(lng))
	if 0 == result then
		latlng = "reqLbsLoc=1&lat="..lat.."&lng="..lng
	end
	log.info("getLocCb:",latlng)
    --return result,lat,lng
    --获取经纬度成功
    --if result==0 then
    --失败
end
]]


socket.setDnsParser(
    function(domainName,token)
        http.request("GET","119.29.29.29/d?dn="..domainName,nil,nil,nil,35000,
            function (result,statusCode,head,body)
                log.info("testHttp..httpDnsCb",result,statusCode,head,body)
                if result and statusCode=="200" and body and body:match("^[%d%.]+") then
                    sys.publish("USER_DNS_PARSE_RESULT_"..token,(body:match("^([%d%.]+)")))
                else
                    sys.publish("USER_DNS_PARSE_RESULT_"..token)
                end
            end)        
    end
)


local ADC_ID = 0

--- ADC读取测试
-- @return 无
-- @usage read()
local function read_adc()
    -- 打开adc
    adc.open(ADC_ID)
    -- 读取adc
    -- adcval为number类型，表示adc的原始值，无效值为0xFFFF
    -- voltval为number类型，表示转换后的电压值，单位为毫伏，无效值为0xFFFF；adc.read接口返回的voltval放大了3倍，所以需要除以3还原成原始电压
    local adcval,voltval = adc.read(ADC_ID)
    log.info("testAdc.read",adcval,(voltval-(voltval%3))/3,voltval)
    --如果adcval有效
    if adcval and adcval~=0xFFFF then
    end
    --如果voltval有效	
    if voltval and voltval~=0xFFFF then
        --adc.read接口返回的voltval放大了3倍，所以此处除以3
        voltval = (voltval-(voltval%3))/3
    end
    adc.close(ADC_ID)
end

local i2cid = 2
--[[
read rtc time,return arrow as{sec,min,hour,day,weekday,mon,year}
]]
local function read_rtc_time()
	local i2cslaveaddr = 0x0E
	if i2c.setup(i2cid,i2c.SLOW,i2cslaveaddr) ~= i2c.SLOW then
        print("testI2c.init1 fail")
        return
    end
	--i2c.write(i2cid,2,1)
	local _rtc_time = i2c.read(i2cid,2,7)
	i2c.close( i2cid )
	for i=1,7,1 do
		print("testI2c.init1",string.format("%02X",1+i,_rtc_time[i]),string.toHex(_rtc_time))
	end
	return _rtc_time
end
--[[
read rtc alarm time,return arrow as {min,hour,day,weekday}
]]
local function read_rtc_alarm()
	local i2cslaveaddr = 0x0E
	if i2c.setup(i2cid,i2c.SLOW,i2cslaveaddr) ~= i2c.SLOW then
        print("testI2c.init1 fail")
        return
    end
	--i2c.write(i2cid,2,1)
	local _rtc_time = i2c.read(i2cid,9,4)
	i2c.close( i2cid )
	for i=1,4,1 do 
		print("testI2c.init1",string.format("%02X",8+i,_rtc_time[i]),string.toHex(_rtc_time))
	end
	return _rtc_time
end
--[[write rtc time with arrow{sec,min,hour,day,weekday,mon,year}}]]
local function write_rtc_time(_time_now)
	local i2cslaveaddr = 0x0E
	if i2c.setup(i2cid,i2c.SLOW,i2cslaveaddr) ~= i2c.SLOW then
        print("testI2c.init1 fail")
        return
    end
	for i=1,7,1 do
		i2c.write(i2cid,1+i,_time_now[i])
		print("testI2c.init1",string.format("%02X=%02X",1+i,_time_now[i]),string.toHex(_time_now))
	end
	i2c.close( i2cid )
end

--[[write rtc alarm with arrow{min,hour,day,weekday}}]]
local function write_rtc_alarm(_time_alarm)
	local i2cslaveaddr = 0x0E
	if i2c.setup(i2cid,i2c.SLOW,i2cslaveaddr) ~= i2c.SLOW then
        print("testI2c.init1 fail")
        return
    end
	for i=1,4,1 do
		i2c.write(i2cid,8+i,_time_alarm[i])
		print("testI2c.init1",string.format("%02X=%02X",8+i, _time_alarm[i]),string.toHex(_time_alarm))
	end
	i2c.close( i2cid )
end

--[[
local function reqLbsLoc()   
    lbsLoc.request(getLocCb, nil, 40000)
end

--reqLbsLoc()
]]

sys.taskInit(
    function()
		while true do
			if not socket.isReady() then
				log.info("sys.waitUntil")
				sys.waitUntil("IP_READY_IND",60000) 
			end
			if socket.isReady() then
				--read_adc()
				_http_received = 0
				log.info("socket.isReady")
				CellInfo = "val="..net.getCellInfoExt()
				sn = "sn="..misc.getSn()
				imei = "imei="..misc.getImei()
				rssi = "gsm="..net.getRssi()
				vBatt = misc.getVbatt()
				--sys.wait(10)
				
				_get_str = string.format("%s&%s&%s&batt=%d&%s",sn,imei,rssi,vBatt,CellInfo)
				log.info("GET:".._get_str)
				http.request("GET","http://17533e12u3.iask.in/cgi-bin/get2.sh?".._get_str,nil,nil,nil,3000,cbFnc)
			else
				log.info("not socket.isReady after 40sec")
			end
			local i=0
			while((_http_received == 0)and (i<5)) do
				sys.wait(1000)
				i = i+1
			end
			net.switchFly(true)
			sys.wait(30000)
			net.switchFly(false)
		end
	end
)
--http.request("GET","https://www.baidu.com",{caCert="ca.crt"},nil,nil,nil,cbFnc)
--http.request("GET","www.lua.org",nil,nil,nil,30000,cbFncFile,"download.bin")
--http.request("GET","http://www.lua.org",nil,nil,nil,30000,cbFnc)
--http.request("GET","www.lua.org/about.html",nil,nil,nil,30000,cbFnc)
--http.request("GET","www.lua.org:80/about.html",nil,nil,nil,30000,cbFnc)
--http.request("POST","www.iciba.com",nil,nil,"Luat",30000,cbFnc)
--http.request("POST","36.7.87.100:6500",nil,{head1="value1"},{[1]="begin\r\n",[2]={file="/lua/http.lua"},[3]="end\r\n"},30000,cbFnc)
--http.request("POST","http://lq946.ngrok.xiaomiqiu.cn/",nil,nil,{[1]="begin\r\n",[2]={file_base64="/lua/http.lua"},[3]="end\r\n"},30000,cbFnc)

        

--如下示例代码是利用文件流模式，上传录音文件的demo，使用的URL是随意编造的
--[[
http.request("POST","www.test.com/postTest?imei=1&iccid=2",nil,
         {['Content-Type']="application/octet-stream",['Connection']="keep-alive"},
         {[1]={['file']="/RecDir/rec001"}},
         30000,cbFnc)
]]


--如下示例代码是利用x-www-form-urlencoded模式，上传3个参数，通知openluat的sms平台发送短信
--[[
function urlencodeTab(params)
    local msg = {}
    for k, v in pairs(params) do
        table.insert(msg, string.urlEncode(k) .. '=' .. string.urlEncode(v))
        table.insert(msg, '&')
    end
    table.remove(msg)
    return table.concat(msg)
end

http.request("POST","http://api.openluat.com/sms/send",nil,
         {
             ["Authorization]"="Basic jffdsfdsfdsfdsfjakljfdoiuweonlkdsjdsjapodaskdsf",
             ["Content-Type"]="application/x-www-form-urlencoded",
         },
         urlencodeTab({content="您的煤气检测处于报警状态，请及时通风处理！", phone="13512345678", sign="短信发送方"}),
         30000,cbFnc)
]]
         
         


--如下示例代码是利用multipart/form-data模式，上传2参数和1个照片文件
--[[
local function postMultipartFormData(url,cert,params,timeout,cbFnc,rcvFileName)
    local boundary,body,k,v,kk,vv = "--------------------------"..os.time()..rtos.tick(),{}
    
    for k,v in pairs(params) do
        if k=="texts" then
            local bodyText = ""
            for kk,vv in pairs(v) do
                bodyText = bodyText.."--"..boundary.."\r\nContent-Disposition: form-data; name=\""..kk.."\"\r\n\r\n"..vv.."\r\n"
            end
            body[#body+1] = bodyText
        elseif k=="files" then
            local contentType =
            {
                jpg = "image/jpeg",
                jpeg = "image/jpeg",
                png = "image/png",                
            }
            for kk,vv in pairs(v) do
                print(kk,vv)
                body[#body+1] = "--"..boundary.."\r\nContent-Disposition: form-data; name=\""..kk.."\"; filename=\""..kk.."\"\r\nContent-Type: "..contentType[vv:match("%.(%w+)$")].."\r\n\r\n"
                body[#body+1] = {file = vv}
                body[#body+1] = "\r\n"
            end
        end
    end    
    body[#body+1] = "--"..boundary.."--\r\n"
        
    http.request(
        "POST",
        url,
        cert,
        {
            ["Content-Type"] = "multipart/form-data; boundary="..boundary,
            ["Connection"] = "keep-alive"
        },
        body,
        timeout,
        cbFnc,
        rcvFileName
        )    
end

postMultipartFormData(
    "1.202.80.121:4567/api/uploadimage",
    nil,
    {
        texts = 
        {
            ["imei"] = "862991234567890",
            ["time"] = "20180802180345"
        },
        
        files =
        {
            ["logo_color.jpg"] = "/ldata/logo_color.jpg"
        }
    },
    60000,
    cbFnc
)
]]
