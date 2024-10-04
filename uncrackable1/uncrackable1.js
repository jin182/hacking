Java.perform(function () {
  const rooting = Java.use("sg.vantagepoint.uncrackable1.MainActivity$1");
  rooting.onClick.implementation = function (arg1, arg2) {
    console.log("[+] rooting bypass success");
  };

  const check = Java.use("sg.vantagepoint.a.a");
  const arg1 = [
    -115, 18, 118, -124, -53, -61, 124, 23, 97, 109, -128, 108, -11, 4, 115,
    -52,
  ];
  const arg2 = [
    -27, 66, 98, 21, -53, 91, -102, 6, -61, -96, -75, -26, -92, -67, 118, -102,
    73, -24, -16, 116, -8, 46, -1, 29, -107, -85, 124, 23, 20, 118, 24, -25,
  ];
  let flag = "";
  const result = check.a(arg1, arg2);
  for (let i = 0; i < result.length; i++) {
    flag += String.fromCharCode(result[i]);
  }
  console.log(flag);
});
