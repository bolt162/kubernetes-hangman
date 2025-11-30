# Enterprise-SW-Plat-Assignment-1

To complete the 2nd and 3rd part of this assignment, I made a hangman game using flask and hosted it locally on a docker container.

# Part #2

## I created a Dockerfile as seen in the repo above and built the docker image using:

docker build -t bolt162/hangman:latest .

<img width="1260" height="618" alt="Screenshot 2025-09-14 at 1 53 56 PM" src="https://github.com/user-attachments/assets/88ababa2-f0f4-4a8d-a5fe-98534e911f31" />


## The second step was to write down unit tests and run them to ensure that the game does not have edge cases where the applicaiton would crash. The test files are available in the tests/ repository and I ran the following command to run those tests:

docker run —rm bolt162/hangman: latest python -m unittest discover -s tests

<img width="1279" height="130" alt="Screenshot 2025-09-14 at 1 59 35 PM" src="https://github.com/user-attachments/assets/62b4706c-6624-44be-a134-7ddecf4f8bb2" />


## The last step was to push the image to the registry with:

docker push bolt162/hangman:latest

<img width="774" height="229" alt="Screenshot 2025-09-14 at 2 05 46 PM" src="https://github.com/user-attachments/assets/f37834cb-a6a1-4670-a81e-00700f3da3af" />

# Part #3 (Performance difference VM vs Docker)

## To automate a Virtual Machine setup, we used Vagrand:
vagrant up
vagrant ssh
cd /vagrant
python3 hangman.py

## Then i used htop to monitor stats in both vagrand and docker
<img width="711" height="365" alt="Screenshot 2025-09-14 at 7 38 45 PM" src="https://github.com/user-attachments/assets/337dd55c-5663-456e-a6c5-cff5449c25a0" />


## Request Throughput/Response Time: Used ab (ApacheBench) for load testing: ab -n 1000 -c 10 http://ip:port/

Vagrant:

<img width="685" height="757" alt="Screenshot 2025-09-14 at 7 39 40 PM" src="https://github.com/user-attachments/assets/05f18e71-48ef-4fdb-94b2-bf572d73446a" />
<img width="681" height="345" alt="Screenshot 2025-09-14 at 7 39 50 PM" src="https://github.com/user-attachments/assets/35c40c0c-8a16-420f-8508-6a82bcf86bfe" />

Docker:

<img width="683" height="148" alt="Screenshot 2025-09-14 at 7 40 06 PM" src="https://github.com/user-attachments/assets/9254a8c0-f5ac-4446-a0e5-752e045664c2" />
<img width="683" height="754" alt="Screenshot 2025-09-14 at 7 40 15 PM" src="https://github.com/user-attachments/assets/bf0ea8b2-5a60-4bcd-bae9-9e69ded13971" />


## Benchmark Results: Hangman Application (Docker vs. Vagrant VM)

| Metric | Docker | Vagrant VM | Difference/Notes |
|--------|--------|-------------|------------------|
| Server Software | Werkzeug/3.1.3 | Werkzeug/2.0.3 | Different versions; may affect performance. |
| Port | 4000 | 5000 | N/A |
| Document Length | 5521 bytes | 1319 bytes | Docker serves larger responses. |
| Time Taken | 2.633 s | 20.220 s | Docker ~7.7x faster. |
| Complete Requests | 1000 | 1000 | Identical. |
| Failed Requests | 0 | 1 (Length: 1) | Vagrant had one failure. |
| Total Transferred | 5,859,000 bytes | 1,508,334 bytes | Higher in Docker due to document size. |
| HTML Transferred | 5,521,000 bytes | 1,353,297 bytes | Higher in Docker due to document size. |
| Requests per Second | 379.72 [#/sec] | 49.46 [#/sec] | Docker ~7.7x higher throughput. |
| Time per Request (mean) | 26.335 ms | 202.197 ms | Docker ~7.7x faster. |
| Time per Request (concurrent) | 2.633 ms | 20.220 ms | Docker ~7.7x faster. |
| Transfer Rate | 2172.65 KB/s | 72.85 KB/s | Docker ~29.8x higher. |
| Connect Time (min/mean/sd/max) | 0/0.6/0/18 ms | 0/0.6/0.6/13 ms | Similar; negligible differences. |
| Processing Time (min/mean/sd/max) | 15/26/6.1/73 ms | 92/201/46.4/612 ms | Docker faster, less variable. |
| Waiting Time (min/mean/sd/max) | 2/12/5.4/46 ms | 91/195/45.3/612 ms | Docker lower latency. |
| Total Time (min/mean/sd/max) | 15/26/6.1/73 ms | 92/201/46.4/612 ms | Docker ~7.7x lower mean time. |
| Latency Percentiles | Not provided | 50%: 200 ms, 75%: 226 ms, 90%: 259 ms, 95%: 279 ms | Vagrant higher tail latencies. |

## Conclusion
The Hangman application performs significantly better in Docker, with ~7.7x higher requests per second, lower latency, and faster test completion with no failed requests. Docker's lightweight containerization likely reduces overhead compared to Vagrant's VM setup. Differences may also stem from Werkzeug versions or configurations. Docker appears more scalable, but additional tests with identical setups or varied loads are recommended.
