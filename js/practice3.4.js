function ElectricalDevice(name, amper){
	this.name = name;
	this.amper = amper;
	this.watt = this.amper * 235;
	this.plug = false;
}
ElectricalDevice.prototype.getWatt = function(){
	if(this.plug){
		console.log(`Device ${this.name} have ${this.watt} power watt`)
	}
	else{
		console.log(`Device ${this.name} no plug`)

	}
}


function Computer(brand, name){
	this.brand = brand;
	this.name = name;
}


Computer.prototype = new ElectricalDevice();
Computer.prototype.on = function(){
	
	if (this.plug)
	{
			console.log(`Идет загрузка ${this.name}`)
	}
	else
		{
			console.log(`Прибор выключен`)
		}
}

function Lampa(brand, name){
	this.brand = brand;
	this.name = name;
	}


Lampa.prototype = new ElectricalDevice();
Lampa.prototype.on = function(){
	if (this.plug){
		console.log(`Прибор ${this.name} излучает свет`)
	}
	else
	{console.log(`Прибор выключен`)
	}
}



const lampa = new Lampa('Vision', 'Светильник', 0.05);
const computer = new Computer('IBM','Комп', 2.6);

lampa.getWatt();
computer.getWatt();
lampa.on();
computer.on();

	for (let item of [lampa, computer]){
		item.plug = true
	}

lampa.on();
computer.on();
	