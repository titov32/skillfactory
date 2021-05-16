class ElectricalDevice{
	constructor(name, amper, plug){
	this.name = name;
	this.amper = amper;
	this.watt = this.amper * 230; //today standard in Russia
	this.plug = false;
	}
	getWatt(){
			if(this.plug){
		console.log(`Устройство ${this.name} имеет мощность ${this.watt} ватт`);
		}
		else{
			console.log(`Device ${this.name} no plug`);
		}
	}
}

class Computer extends ElectricalDevice{
	constructor(brand, plug, amper, formFactor){
		super(plug, amper);

		this.brand = brand;
		this.formFactor = formFactor;
	}

	on (){
		if (this.plug){
				console.log(`Идет загрузка ${this.name}`)
		}
		else
			{console.log(`Прибор выключен`)
		}
	}
}

class Lampa extends ElectricalDevice{
	constructor(brand, plug, amper, color){
		super(plug, amper);
		this.brand = brand;
		this.color = color;
	}

	on (){
		if (this.plug){
			console.log(`Прибор ${this.name} излучает свет`)
		}
		else
		{console.log(`Прибор выключен`)
		}
	}
}


const lampa = new Lampa('Vision', 'Светильник', 0.05, 'белый');
const computer = new Computer('IBM','Комп', 2.6, 'notebook');

lampa.getWatt();
computer.getWatt();
lampa.on();
computer.on();
console.log('Включаем приборы в сеть')
	for (let item of [lampa, computer]){
		item.plug = true;
		item.on();
		item.getWatt();
	}
