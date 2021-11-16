const ENV = process.env.docker == null;

const localhost = window.location.hostname;
console.log(window.location);
export const API_URL = `http://${ENV ? localhost : "mediator-api"}:8011/`;

console.log(API_URL);
