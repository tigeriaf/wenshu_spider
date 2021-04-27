function cipher() {
    var info = {};
	var date = new Date();
	var timestamp = date.getTime().toString();
	var salt = rand_str(24);
	var year = date.getFullYear().toString();
	var month = (date.getMonth() + 1 < 10 ? "0" + (date.getMonth() + 1) : date.getMonth()).toString();
	var day = (date.getDate() < 10 ? "0" + date.getDate() : date.getDate()).toString();
	var iv = year + month + day;
	info["timestamp"] = timestamp
	info["salt"] = salt
	info["iv"] = iv
	info["date"] = date
	return info

function rand_str(size){
        var str = "",
        arr = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'];
        for(var i=0; i<size; i++){
            str += arr[Math.round(Math.random() * (arr.length-1))];
        }
        return str;
    }
};

function strTobinary(str) {
	var result = [];
	var list = str.split("");
	for (var i = 0; i < list.length; i++) {
		if (i != 0) {
			result.push(" ");
		}
		var item = list[i];
		var binaryStr = item.charCodeAt().toString(2);
		result.push(binaryStr);
	};
	return result.join("");
}