import mysql from "mysql2"

const pool = mysql.createPool({
    host: "localhost",
    port: 3306,
    user: "root",
    database: "mydb",
    password: process.env.DATABASE_PASSWORD,
    waitForConnections: true,
    connectionLimit: 10,
    queueLimit: 0
})

const promisePool = pool.promise()

export default promisePool;