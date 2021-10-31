const ENV = process.env.docker == null;

export const API_URL = `http://${ENV ? "localhost" : "mediator-api"}:8011/`;
