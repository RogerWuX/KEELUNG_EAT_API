
var jqueryScriptElement = document.createElement('script'); 
jqueryScriptElement.src = 'jquery3.4.js';
jqueryScriptElement.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(jqueryScriptElement);

var socketIOScriptElement = document.createElement('script'); 
socketIOScriptElement.src = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'
socketIOScriptElement.type = 'text/javascript';
document.getElementsByTagName('head')[0].appendChild(socketIOScriptElement); 
function createButton(buttonName,id,onclickFunctionName)
{
	var button=document.createElement("button");
	button.innerHTML=buttonName;
	button.id=id;
	button.onclick=onclickFunctionName;
	document.body.appendChild(button);
	
}

var ajaxTestInfos=[
{
	buttonName:"註冊",
	url:'http://127.0.0.1:5000/register',
	type:"POST",
	data:{
	  name: "GG",
	  email: "gg@gmail.com",
	  password: "ee",
	  district: "中正區",
	  address: "北寧路2號",
	  identity: "0",
	  status:"0",
	  tel: "0955334119"
	}
},
{
	buttonName:"登入",
	url:'http://127.0.0.1:5000/login',
	type:"POST",
	data:{
		email: "cc@gmail.com",
		password: "aa"	
	}
},
{
	buttonName:"新增訂單",
	url:'http://127.0.0.1:5000/order',
	type:"POST",
	data:{
		recieve_time:'2019-05-06 07:00:00',

		district:'中正區',
		address:'北寧路2號',
		consumer_id:'5dc3c34ff1733b1e786c8389',
		store_id:'5dc3c34ff1733b1e786c8388',
		foods:[
		{
			food_id:'5dc3c34ff1733b1e786c8388',
			number:5
		}			
		]
		
		
	}
},
{
	buttonName:"外送員查看目前訂單",
	url:'http://localhost:5000/delivery/5dc3c34ff1733b1e786c8389/current_orders',
	type:"GET",
	data:'5dc3c34ff1733b1e786c8389'
},
{
	buttonName:"顧客查看目前訂單",
	url:'http://localhost:5000/consumer/5dc3c34ff1733b1e786c8389/current_orders',
	type:"GET",
	data:'5dc3c34ff1733b1e786c8389'
}
]

var socketTestInfos=[
{
	namespace:'admin',
	connect_button:'管理員訂單管理_連接',
	query_parameter:{token:'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3NjA3OTM3OCwiZXhwIjoxNTc2MDc5OTc4fQ.eyJpZCI6IjVkZjEwZmVlNGI4ODZjNzE0NGEzMTM2OCJ9.WnIZDTpLIjcOThshafKDkUEH5mKMLEJXdGGSmmRW3S5oCMIBynZvnpTbyBkqrzduQJlX6DteEZIw5viL4giGww'},
	event_handlers:[
	{
		event_name:'connect',
		handler:function(){console.log('admin namespace connect established')}
	},
	{
		event_name:'order_data',
		handler:function(data){console.log(data)}
	}
	,
	{
		event_name:'order_state_update',
		handler:function(data){console.log(data)}
	}
	,
	{
		event_name:'order_delete',
		handler:function(data){console.log(data)}
	}],
	action:[
	{
		name:'管理員更新訂單狀態',
		event_name:'order_state_update',
		data:{
			order_id:'5dc3c34ff1733b1e786c8388',
			delivery_state:'pending',
			store_state:'confirmed'
		}
	},
	{
		name:'管理員刪除訂單',
		event_name:'order_delete',
		data:'5dc3c34ff1733b1e786c8388'
	}
	]
		
	
},
{
	namespace:'delivery_man',
	connect_button:'外送員待接受訂單檢視_連接',
	query_parameter:{token:'vvvvvvv'},
	event_handlers:[
	{
		event_name:'connect',
		handler:function(){console.log('delivery_man namespace connect established')}
	},
	{
		event_name:'order_data',
		handler:function(data){console.log(data)}
	},
	{
		event_name:'order_accept',
		handler:function(data){console.log(data)}
	}],
	action:[
	{
		name:'外送員接受訂單',
		event_name:'order_accept',
		data:'5dc3c34ff1733b1e786c8388'
	}
	]
		
	
}
,
{
	namespace:'restaurant',
	connect_button:'餐廳待處理訂單檢視_連接',
	query_parameter:{token:'eyJhbGciOiJIUzUxMiIsImlhdCI6MTU3NjA3NDE0MCwiZXhwIjoxNTc2MDc0NzQwfQ.eyJpZCI6IjVkZGJkZDEyNWI0NDIzNzBkNDZhMzZlZSJ9.f9HxBeCCbbCUIti_YGLM2KLt23z-JxeslE15htj7vidVWWjduYX6XcVMTFoPk3HOcRNuRj-zK5dOkhLtgKKXSg'},
	event_handlers:[
	{
		event_name:'connect',
		handler:function(){console.log('restaurant namespace connect established')}
	},
	{
		event_name:'order_data',
		handler:function(data){console.log(data)}
	},
	{
		event_name:'order_confirm',
		handler:function(data){console.log(data)}
	}],
	action:[
	{
		name:'餐廳確認訂單',
		event_name:'order_confirm',
		data:'5dc3c34ff1733b1e786c8388'
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
	  data:JSON.stringify(ajaxTestInfos[index].data),
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
		createButton(socketTestInfos[i].connect_button,'wsConnect_'+i,socketConnect)
		for(var j =0;j<socketTestInfos[i].action.length;j++)
		{
			createButton(socketTestInfos[i].action[j].name,'wsEmit_'+i+'_'+j,socketEmit)
		}
	}
}
function socketConnect()
{
	var index=this.id.split('_')[1]
	console.log('http://localhost:5000/'+socketTestInfos[index].namespace)
	var socket = io('http://localhost:5000/'+socketTestInfos[index].namespace,{query:socketTestInfos[index].query_parameter});
	var event_handlers=socketTestInfos[index].event_handlers
	for(var i=0;i<event_handlers.length;++i)
	{		
		socket.on(event_handlers[i].event_name,event_handlers[i].handler);
	}
	socketTestInfos[index].socket=socket
	
}
function socketEmit()
{
	let args=this.id.split('_');
	let i=args[1];console.log(i);
	let j=args[2];console.log(j);
	console.log(socketTestInfos[i].action[j].event_name)
	console.log(socketTestInfos[i].action[j].data)
	socketTestInfos[i].socket.emit(socketTestInfos[i].action[j].event_name,socketTestInfos[i].action[j].data)
}
function init()
{
	initAjaxTest();
	initSocketTest();
	
}
