import fetch from 'node-fetch';
import { URLSearchParams } from 'url';
import { readFileSync, writeFileSync } from 'fs';
import { createDecipheriv, createHash } from 'crypto';

const config = JSON.parse(readFileSync('external_api.config.json'));

/** 国家电网（北京）接口 */
const sgcc_api = async (path, init={}) => {
  if (init.headers === undefined) {
    init.headers = {};
  }
  init.headers['User-Agent'] = config.sgcc.ua;
  init.headers['Cookie'] = `user_openid=${config.sgcc.open_id}`;

  const res = await fetch(`${config.sgcc.endpoint}${path}`, init);
  return await res.json();
};

/** 北京自来水集团接口 */
const randomString = (e, r, t) => {
  var n = "", a = r, s = [ "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z", "A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z" ];
  e && (a = Math.round(Math.random() * (t - r)) + r);
  for (var o = 0; o < a; o++) {
      n += s[Math.round(Math.random() * (s.length - 1))];
  }
  return n;
};

const parameterSort = (e) => {
  var r, t = [];
  for (var n in e) {
      var a = n + "=" + e[n] + "&";
      t.push(a);
  }
  return ((r = t).sort(function(e, r) {
      return e.localeCompare(r);
  }), r).join("");
};

const decryptResponse = (ct) => {
  const key = Buffer.from(config.bjwater.secret_key.slice(0, 16), 'utf8');
  const decipher = createDecipheriv('aes-128-ecb', key, null);
  let decrypted = decipher.update(ct, 'base64', 'utf8');
  decrypted += decipher.final('utf8');
  return decrypted;
};

const bjwater_api = async (path, query={}) => {
  query.timestamp = new Date().getTime();
  query.nonce = randomString(!0, 10, 32).toString();
  query.userCode = config.bjwater.user_code;
  let queryStr = parameterSort(query);
  queryStr = queryStr.substring(0, queryStr.lastIndexOf("&"));
  queryStr += `&secretKey=${config.bjwater.secret_key}${config.bjwater.md5_salt}`;
  const sign = createHash('md5').update(queryStr).digest('hex').toUpperCase();
  query.sign = sign;
  query.noEncrypt = '';

  return await fetch(`${config.bjwater.endpoint}${path}?${new URLSearchParams(query).toString()}`, {
    headers: {
      token: config.bjwater.token
    }
  }).then(r => r.json())
    .then(ct => decryptResponse(ct.data))
    .then(pt => JSON.parse(pt));
};

/** 获取国家电网数据 */
const fetchSGCCData = async () => {
  const sgcc_data = {
    overview: null,
    daily: null, 
    monthly: null,
    payment: null,
    updateTime: new Date().getTime()
  };
  
  // 用电概览
  const overview = await sgcc_api(`/home/getElectricBill?consNo=${config.sgcc.cons_no}`);
  if (overview.status === 0) {
    sgcc_data.overview = overview.data;
  }
  
  // 每日用电
  let params = new URLSearchParams();
  params.append('consNo', config.sgcc.cons_no);
  params.append('days', 30);
  const daily = await sgcc_api('/electric/bill/daily', {
    method: 'POST',
    body: params
  });
  if (daily.status === 0) {
    sgcc_data.daily = daily.data;
  }
  
  // 月度用电
  params = new URLSearchParams();
  params.append('consNo', config.sgcc.cons_no);
  params.append('currentYear', new Date().getFullYear());
  params.append('isFlag', 1);
  const monthly = await sgcc_api('/electric/bill/queryElecBillInfoEveryYear', {
    method: 'POST',
    body: params
  });
  if (monthly.status === 0) {
    sgcc_data.monthly = monthly.data;
  }
  
  // 缴费记录
  let currentDate = new Date();
  const offset = currentDate.getTimezoneOffset();
  currentDate = new Date(currentDate.getTime() - (offset*60*1000));
  
  params = new URLSearchParams();
  params.append('consNo', config.sgcc.cons_no);
  params.append('orgNo', config.sgcc.org_no);
  params.append('endTime', currentDate.toISOString().split('T')[0]);
  currentDate.setFullYear(currentDate.getFullYear() - 1);
  params.append('startTime', currentDate.toISOString().split('T')[0]);
  const payment = await sgcc_api('/payment/monthly/chart', {
    method: 'POST',
    body: params
  });
  if (payment.status === 0) {
    sgcc_data.payment = payment.data;
  }

  return sgcc_data;
};

/** 获取用水数据 */
const fetchBJWaterData = async () => {
  const bjwater_data = {
    analysis: null,
    payment: null,
    radar: null,
    yearly: {},
    monthly: {},
    updateTime: new Date().getTime()
  };
  bjwater_data.analysis = await bjwater_api('/getWaterAnalysis');
  bjwater_data.payment = await bjwater_api('/paymentRecord');
  bjwater_data.radar = await bjwater_api('/getWaterRadar');
  const entries = await bjwater_api('/getMonthsAndYears');
  for (let i = 0; i < entries.years.length; i++) {
    const year = entries.years[i];
    bjwater_data.yearly[year] = await bjwater_api('/getAnnualBill', { year: year });
  }
  for (let i = 0; i < entries.months.length; i++) {
    const month = entries.months[i];
    bjwater_data.monthly[month] = await bjwater_api('/getMonthlyBill', { billDate: month });
  }
  return bjwater_data;
};

/** crontab 每日执行更新 */
const sgcc_data = await fetchSGCCData();
writeFileSync('sgcc.data.json', JSON.stringify(sgcc_data));
// 用水信息每周一更新
if ((new Date().getDay()) === 1) {
  const bjwater_data = await fetchBJWaterData();
  writeFileSync('bjwater.data.json', JSON.stringify(bjwater_data));
}
