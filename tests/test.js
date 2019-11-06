
var jqueryScriptElement = document.createElement('script'); 
jqueryScriptElement.src = 'jquery3.4.js';
jqueryScriptElement.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(jqueryScriptElement);

var socketIOScriptElement = document.createElement('script'); 
socketIOScriptElement.src = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'
socketIOScriptElement.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(socketIOScriptElement); 


var ajaxTestInfos=[
{
	buttonName:"新增訂單",
	url:'http://localhost:5000/order',
	type:"POST",
	data:{
		'order_name':'gg662'
	}	
},
{
	buttonName:"查詢所有訂單",
	url:'http://localhost:5000/order',
	type:"GET",
	data:{
	}	
}
]

var socketTestInfos=[
{
	namespace:'admin',
	connect_button:'所有訂單_連接',
	event_handlers:
				[
				{
					'event_name':'connect',
					'handler':function(){console.log('connect established')}
				},
				{
					'event_name':'order_data',
					'handler':function(data){console.log(data)}
				}
				]
	
}
]

function initAjaxTest()
{
	
	for(var i=0;i<ajaxTestInfos.length;++i)
	{
		var button=document.createElement("button");
		button.innerHTML=ajaxTestInfos[i].buttonName;
		button.id='ajax_'+i		
		button.onclick=sendAjaxData;
		document.body.appendChild(button);
	}
	
}
function sendAjaxData()
{
	index=this.id.split('_')[1];
	
	console.log(ajaxTestInfos[index].url);
	console.log(ajaxTestInfos[index].data);
	$.ajax({
	  async: false,
	  url: ajaxTestInfos[index].url,
	  contentType: 'application/json; charset=UTF-8',
	  type: ajaxTestInfos[index].type,
	  dataType: "json",
	  data:ajaxTestInfos[index].data,
	  success: function(response) {
		console.log(response);
	  },
	  
	  error: function() {
		console.log("error");
	  }
	});	
}

function initSocketTest()
{
	for(var i=0;i<socketTestInfos.length;++i)
	{
		
		var button=document.createElement("button");
		button.innerHTML=socketTestInfos[i].connect_button;
		button.id='wsConnect_'+i		
		button.onclick=socketConnect;
		document.body.appendChild(button);
	}
}
function socketConnect()
{
	var index=this.id.split('_')[1]
	var socket = io('http://localhost:5000/'+socketTestInfos[index].namespace);
	var event_handlers=socketTestInfos[index].event_handlers
	for(var i=0;i<event_handlers.length;++i)
	{		
		socket.on(event_handlers[i].event_name,event_handlers[i].handler);
	}

    /*socket.on('connect', function() {
       console.log('success');
    });
	socket.on('close', function() {
       console.log('close');
    });
	socket.on('message',function(data){
		console.log(data)
	});
	socket.on('not_assigned_orders',function(data){
		console.log(data)
	});*/
	


	
}
function init()
{
	initAjaxTest();
	initSocketTest();
	
}
