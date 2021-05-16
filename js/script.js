//alert('hello world');
let a=prompt('Input num')
console.log(a);
console.log('typeof a', typeof a);
if (typeof a=='string')
	console.log('a string');

let b = typeof a;
switch (b){
	case 'string':
		console.log("Это строка");
		break;
	case 'number':
		console.log("Это number");
		break;
	case 'boolean':
		console.log("Это boolean");
		break;
	default:
		console.log("Это тип не определен");
}



/*
console.log('Делаем преобразование')

a= Number(a)
console.log('проверяем еще раз')
if (typeof a=='string')
	console.log('a string');
else
	console.log('a number');
let chetnoe=(a%2==0)?'Четное':'Не Четное'
console.log(chetnoe);

*/

arr = [1,2,3,4,5,6,0];

function isEven(arr){
	arr.forEach(function(item, index, array){
		if (item==0){
			console.log(`item ${item} index ${index} равен нулю`)
		}
		else if (item%2===0){
			console.log(`item ${item} index ${index} четный`)
		}
		else{
			console.log(`item ${item} index ${index} нечетный`)
		};
});
}
console.log('Выводим работу функции')
isEven(arr);


for (let i = 0; i < arr.length; i++) 
{
	let temp_arr=arr.slice((i+1), arr.length);
	if (arr[i] in temp_arr)
	{
		console.log(`Элемент '${arr[i]}' имеет дубль`)
		console.log(`поиск был в ${temp_arr}`)
	};
};

let hash_table = new Map();
hash_table.set(1,'qwerty');
hash_table.set('qaz','wsx');
hash_table.set(true,'asdfg');

console.log(hash_table.values())