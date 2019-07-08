Getting Started with MariaDB Galera and MariaDB MaxScale on CentOS 7.x

## Mục lục

---------------------------------------------

### [I Giới thiệu](#I)
- [1. Mariadb](#1)
- [2 Galera Cluster](#2)
- [3 MariaDB MaxScale](#3)

### [II. Cài đặt và cấu hình](#II)
- [2.1 Cài đặt python3.6](#2.1)
- [2.2 Install Mariadb](#2.2)
- [2.3 Cầu hình cluster](#2.3)
- [2.4 Cấu hình Max_scale ](#2.4)

### [III Tham khảo](#3)
- [3.1 Liên hệ](#3.1)
________________________________________________________________


### <a name="I"><a/>I Giới thiệu

##### <a name="1"><a/>1 MariaDB.
    
   - MariaDB là gì?
   
     - MariaDB là một nhánh của MySQL( một trong những CSDL phổ biến trên thế giới ), là máy chủ cơ sở dữ liệu cung cấp các chức năng thay thế cho MySQL. MariaDB được xây dựng bởi một số tác giả sáng lập ra MySQL được sự hỗ trợ của đông đảo cộng đồng các nhà phát triển phần mềm mã nguồn mở. Ngoài việc kế thừa các chức năng cốt lõi của MySQL, MariaDB cung cấp thêm nhiều tính năng cải tiến về cơ chế lưu trữ, tối ưu máy chủ.

     - MariaDB phát hành phiên bản đầu tiên vào 11/2008 bởi Monty Widenius, người đồng sáng lập MySQL. Widenius sau khi nghỉ công tác cho MySQL ( sau khi Sun mua lại MySQL ) đã thành lập công ty Monty Program AB và phát triển MariaDB.

   - So sánh MariaDB và Mysql

     - Do sự tương thích giữa MariaDB và MySQL nên trong hầu hết trường hợp chúng ta có thể xóa bỏ MySQL và cài đặt MariaDB để thay thế mà hệ thống vẫn hoạt động bình thường. Trên MariaDB và MySQL có:

        + Data and table definition files (.frm) files hoàn toàn tương thích
        
        + Tất cả client APIs, protocols and structs hoàn toàn giống nhau
        
        + Tất cả filenames, binaries, paths, ports, sockets,... hoàn toàn giống nhau
        
        + Tất cả MySQL connectors (PHP, Perl, Python, Java, .NET, MyODBC, Ruby, MySQL C connector etc) đều hoạt động bình thường khi đổi qua MariaDB
        
        + Gói mysql-client cũng hoạt động khi dùng với MariaDB
        
   - Ngoài việc hỗ trợ các storage engines cơ bản như MyISAM, BLACKHOLE, CSV, MEMORY, ARCHIVE, and MERGE thì trên MariaDB còn bổ sung thêm các storage engines sau:

        + Aria (được xem như một phiên bản cập nhập của MyISAM)
        
        + XtraDB (thay thế cho InnoDB)
        
        + FederatedX
        
        + OQGRAPH
        
        + SphinxSE
        
        + IBMDB2I
        
        + TokuDB
        
        + Cassandra
        
        + CONNECT
        
        + SEQUENCE
        
        + Spider
        
        + PBXT
        
        - Tìm hiểu thêm <a href="https://mariadb.com/kb/en/mariadb/mariadb-vs-mysql-features/" rel="nofollow">tại đây<a>

##### <a name="2"><a/>2 Galera Cluster.

   - Galera Cluster là gì ?

       - Galera cluster là một giải pháp multi master cho database. Sử dụng galera cluster, application có thể read/write trên bất cứ node nào. Một node có thể được thêm vào cluster cũng như gỡ ra khỏi cluster mà không có downtime dịch vụ, cách thức cũng đơn giản.

       - Bản thân các database như mariadb, percona xtradb không có tính năng multi master được tích hợp sẵn bên trong. Các database này sẽ sử dụng một galera replication plugin để sử dụng tính năng multi master do galera cluster cung cấp. Về bản chất, galera replication plugin sử dụng một phiên bản mở rộng của mysql replication api, bản mở rộng này có tên là wsrep api.

       - Dùng wsrep api, galera cluster sẽ thực hiện được certification based replication, một kỹ thuật cho phép thực hiện multi master trên nhiều node. Một writeset, chính là một transaction cần được replication trên các node.
        
   - Lợi ích

       - Một giải pháp multi master hoàn chỉnh nên cho phép read/write trên node bất kỳ
       
       - Synchronous replication.
       
       - Multi thread slave cho phép apply writeset nhanh hơn
       
       - Không cần failover vì node nào cũng là master rồi.
       
       - Automatic node provisioning: Bản thân hệ thống database đã tự backup cho nhau. Tuy nhiên, khả năng backup tự nhiên của galera cluster không loại trừ được các sự cố do con người gây ra như xóa nhầm data.
       
       - Hỗ trợ innodb/XtraDB.
       
       - Hoàn toàn trong suốt với application nên application không cần sửa đổi gì
       
       - Không có Single point of failure vì bất cứ node nào trong hệ cluster cũng là master.
       
   - Hạn chế

       - Không scale up về dung lượng. Một galera cluster có ba node thì cả ba node đó cùng có một data giống hệt nhau. Dung lượng lưu trữ của cả cluster sẽ phụ thuộc vào khả năng lưu trữ trên từng node.
       
       - Không hỗ trợ MyISAM, chuyển đổi một database sử dụng các myisam table sang innodb để sử dụng galera cluster sẽ khó khăn.
       
       - Vẫn có hiện tượng stale data do bất đồng bộ khi apply writeset trên các node.
       
   - Yêu cầu bắt buộc

       - Chỉ hỗ trợ innodb. Đây là yêu cầu thiết kế cơ sở dữ liệu.
       
       - Yêu cầu các node có cấu hình tương đương nhau
       
       - binlog_format phải là row. Cũng giống mysql replication, bạn không được thay đổi binlog_format khi hệ thống galera cluster đang chạy vì có thể làm crash toàn bộ cluster. Yêu cầu bắt buộc này thực ra cũng đem lại một hạn chế. Không phải tự dưng, mysql replication khuyến khích người dùng sử dụng mix binlog_format. Một số transaction ví dụ như delete 10000 rows thì replicate 10000 rows xem ra không tốt bằng replicate đúng một statement delete 10000 rows.

       - flush privileges command không được replicate
       
       - chỉ hỗ trợ flush tables with read lock
       
       - Với engine MyISAM thì chỉ các DDL command CREATE USER mới được replicate
       
       - Transaction size từ 128K đến tối đa 1G theo mặc định, admin có thể mở rộng giới hạn này.
       
       - Mọi bản ghi phải có primary key (multi column primary key cũng được support), không hỗ trợ delete bản ghi không có primary key, các dòng do không có primary key sẽ có thứ tự khác nhau giữa các node. Đây là yêu cầu cho thiết kế cơ sở dữ liệu.
       
       - Query log phải đổ vào file, không thể đổ vào table được.
       
##### <a name="3"><a/>3. MariaDB MaxScale.

   - Maxscale là gì ?

       - Có hai mô hình cân bằng tải: lớp transport và lớp application. HAProxy là một cân bằng tải TCP tuyệt vời, nhưng nó lại có những hạn chế về khả năng của mình để giải quyết các vấn đề mở rộng quy mô nhất định trong môi trường cơ sở dữ liệu phân tán. Trong thế giới mã nguồn mở, có được một vài cân bằng tải cho SQL, cụ thể là MySQL Proxy, ProxySQL và MaxScale, nhưng tất cả đều là bản beta và không thích hợp để sử dụng trong môi trường production. Vì vậy, trong bài viết này tôi muốn muốn chia sẻ về đội ngũ MariaDB phát hành một phiên bản GA của MaxScale đầu năm nay.
       
       - MariaDB MaxScale là thế hệ tiếp theo database proxy dùng để quản lý an ninh, khả năng mở rộng và tính sẵn sàng cao trong quá trình triển khai. Sử dụng MaxScale, quản lý các tiến trình cơ sở dữ liệu đang chạy mà không gây hại đến hoạt động của ứng dụng. Kiến trúc MariaDB MaxScale được thiết kế để tăng tính linh hoạt và tùy biến.

   - Tại sao lại sử dụng MariaDB MaxScale

       - Bảo vệ cơ sở dữ liệu của bạn

       - MaxScale ngăn chặn các cuộc tấn công bảo mật như SQL injection và DDoS. Cơ sở dữ liệu sẽ luôn luôn là một mục tiêu cho tin tặc tìm cách để truy cập thông tin nhạy cảm. MaxScale giúp giảm thiểu truy cập không mong muốn và cung cấp các tính năng cơ sở dữ liệu tường lửa tiên tiến đảm bảo cơ sở dữ liệu của bạn ở mọi cấp độ.

       - Hỗ trợ SSL end-to-end để truy cập dữ liệu an toàn
       
       - Ngăn chặn các cuộc tấn công SQL injection với whitelist và blacklist
       
       - Giảm thiểu các cuộc tấn công DDoS bằng cách cấu hình quy tắc tỷ lệ hạn chế
       
       - Quản lý Scale-Out

       - Quản lý truy cập 1 cách tập trung. MaxScale là proxy cơ sở dữ liệu, cho phép mở rộng quy mô cơ sở dữ liệu theo chiều ngang trong trường hợp cần bảo trì hệ thống. MariaDB MaxScale cung cấp khả năng mở rộng transaction , khả năng mở rộng dữ liệu và mở rộng binlog thông qua:

       - Thời gian đáp ứng truy vấn nhanh hơn thông qua SQL-aware router
       
       - Sharding dữ liệu đơn giản với định tuyến truy vấn
       
       - Tăng thêm hiệu năng khi mở rộng với Binlog server
       
       - Đảm bảo tính sẵn sàng cao

       - Giảm downtime, MaxScale tự động failover và đồng bộ.


### <a name=II><a/> II Cài Đặt và cấu hình.

   - Sơ đồ
    
        ![image](https://user-images.githubusercontent.com/19284401/60801900-03151d00-a1a2-11e9-9089-8e767ddc1cf4.png)


   - Trước khi bắt đầu các bạn cấu chú ý.
    
        - Đây là cấu hình tối thiếu nhất để có thể chạy được cluser và HAproxy. Các bạn cần đọc thêm ở phần tham khảo dưới cuối đến có thể cấu hình sâu hơn và nắm vững hơn trong qua trình vận hành hệ thống.
        
#### <a name=2.1><a/> 2.1 Cài đặt Python3.x        

   - Phân quyền cho file
    
            cd Max_scale/ && chmod +x installpython3.6.sh
 
   - Cài đặt python 3.x

         ./installpython3.6.sh
         
        ![image](https://user-images.githubusercontent.com/19284401/60779028-62077180-a163-11e9-9927-cea625f7735d.png)
    
       - Sau Khi cài đặt python trên server1 xong. Sẽ yêu cầu nhập ip server2 để tiếp tục tiến hành cài đặt trên server2
       
       - Nhập ip server 2 xong sẽ có thông báo nhập password root của server2 các bạn nhập đầy đủ rồi Enter để quá trình cài đặt được tiếp tục.
       
       ![image](https://user-images.githubusercontent.com/19284401/60779110-b01c7500-a163-11e9-963f-714ad176cc51.png)
       
       - Sau khi cài đặt xong, các bạn sẽ thấy thông về về việc chuyển các file cấu hình sang server2.
  
       ![image](https://user-images.githubusercontent.com/19284401/60779166-e0fcaa00-a163-11e9-80c4-7f65cbb2e03b.png)
    
       - Sau khi cài đặt xong server các bước trên sẽ được lập lại với server3.
    
       ![image](https://user-images.githubusercontent.com/19284401/60779207-0093d280-a164-11e9-803a-9e2ae557e1b2.png)
    
       ![image](https://user-images.githubusercontent.com/19284401/60779239-1e613780-a164-11e9-9d11-69ea4e085606.png)
       
       - Sau khi cài đặt trên server2 và server3 xong thì sẽ cài đặt và chuyển file sang Max_scale.
    
       ![image](https://user-images.githubusercontent.com/19284401/60779258-3df86000-a164-11e9-922e-e857a31e77e3.png)
       
       - Sau khi thực hiện cài đặt và chuyển file cấu hình xong thì server Max_scale sẽ tự động reboot. 
       
       ![image](https://user-images.githubusercontent.com/19284401/60779334-8d3e9080-a164-11e9-8b8c-c4946f7167a3.png)
       
####<a name=2.2><a/> 2.2 Install Mariadb       

   - Quá trình cài đặt và cấu hình **Mariadb** bắt đầu

       ![image](https://user-images.githubusercontent.com/19284401/60779354-a0e9f700-a164-11e9-97aa-98011f3c50aa.png)
    
       - Sau khi cài đặt xong Mariadb, chúng ta sẽ đi cấu hình password root sql.
       
            - Mặc định ban đầu tài khoản sql root sẽ chưa có password. Các bạn cứ thế Enter.
            
       ![image](https://user-images.githubusercontent.com/19284401/60779404-d42c8600-a164-11e9-8ff3-e98d66c14760.png)
    
       - Nó hỏi bạn có muốn thay đổi password root không? Nhấn Y Enter.
    
       ![image](https://user-images.githubusercontent.com/19284401/60779581-7f3d3f80-a165-11e9-972d-05f8dbbc8eee.png)
       
        **Chú ý: khi đặt password sql root trên 2 con server (server1, server2, server3) thì nên đặt giống nhau để quá trình cấu hình cluster không gặp lỗi khi khai bao password sql root.**
                
       - Bước này các bạn từ từ và học hướng dẫn nhé. Bản thân mình viết ra nó, nhưng nhiều lúc quen tay cứ 1 vs 2 vs c nhầm lần.
       
       - Cuối cùng là đặt hostname server(Mình sẽ đặt lần lượt là sql01, sql02, sql03)
       
       ![image](https://user-images.githubusercontent.com/19284401/60779657-bd3a6380-a165-11e9-8281-efcfc80611b5.png)
       
       - Trong phần cấu hình network các bạn sẽ có 2 lựa chọn.
       
            - 1  Mặc định tức là quá trình set IP tĩnh cho host diễn ra 1 cách tự động hoàn toàn, các bạn ko cần làm gì cả (IP được set tĩnh là ip hiện tại của host.).
            
            - 2  Cấu hình network thủ công. Tùy chọn này dành cho host của bạn nào có nhiều hơn 1 interface vậy lý trở lên. Hoặc các bạn muốn đặt lại IP cho host thay vì IP mặc định dhcp đang cấp cho host.
            
       - Sau khi cấu hình Network xong, các bạn sẽ nhận được thông báo nhấn C để reboot.
       
            - Nhấp **c** Enter.
       
       - Cấu hình và cài đặt Mariadb trên server1 xong, Giờ ra sẽ qua cấu hình server2 và server3.
       
       - Để tránh các bạn phải chuyển qua chuyển lại giữa các server nên mình sẽ dùng ssh để thực hiện mọi công viêc.
       
       - Sau khi server1 reboot xong các bạn login lại bằng tài khoản root. Lúc này hostname của server đổi thành **sql01**
       
   - Thực hiện ssh sang server2
   
        ![image](https://user-images.githubusercontent.com/19284401/60783718-0d212680-a176-11e9-8627-1e67a3b891e6.png)

        - IP kia là ip của server2
        
        - List file ra các bạn sẽ thấy có 1 file **install_mariadb.py**
        
                     python3.6 install_mariadb.py
                     
       - Quá trình cài đặt Mariadb bắt đầu, và trình tự diễn ra như trên server1 trước đó
       ![image](https://user-images.githubusercontent.com/19284401/60783809-891b6e80-a176-11e9-914f-64640fed1dea.png)
       
       - Chú ý: **Hãy đặt password sql root giống với bên server1**
       
       ![image](https://user-images.githubusercontent.com/19284401/60783876-cd0e7380-a176-11e9-9233-f0ad2d466ec2.png)
       
   
   - Thực hiện ssh sang server3
   
        ![image](https://user-images.githubusercontent.com/19284401/60783980-3bebcc80-a177-11e9-919e-85b5b8bb5211.png)

        - IP kia là ip của server3
        
        - List file ra các bạn sẽ thấy có 1 file **install_mariadb.py**
        
                     python3.6 install_mariadb.py
                     
       - Quá trình cài đặt Mariadb bắt đầu, và trình tự diễn ra như trên server1 trước đó
       
       ![image](https://user-images.githubusercontent.com/19284401/60783809-891b6e80-a176-11e9-914f-64640fed1dea.png)
       
       - Chú ý: **Hãy đặt password sql root giống với bên server1**
       
       ![image](https://user-images.githubusercontent.com/19284401/60784071-a69d0800-a177-11e9-8bf8-3510e661b754.png)
       
       - Nhớ bấm c để reboot lại server.
   
####<a name=2.3><a/> 2.3 Cầu hình cluster.

   -  Sau khi cài đặt xong trên server3 ssh sẽ mất kết nối, và trở về với sql01(server1)
        
        - Di chuyển vào thư mực Max_scale
   
                    cd Max_scale/ && ll
                    
       ![image](https://user-images.githubusercontent.com/19284401/60784261-6c803600-a178-11e9-892e-c155786ab455.png)
       
       - Tiến hành chạy file **config_mariadb.py**
       
                        python3.6 config_mariadb.py
                        
       ![image](https://user-images.githubusercontent.com/19284401/60784733-49ef1c80-a17a-11e9-9a21-c6c74ef8aef0.png)
       
       - Sau khi chạy lênh trên các bạn sẽ được yêu cầu nhập IP, Hostname của server2(sql02),server3(sql03),Max_scale. Các thông tin này sẽ được dùng để cấu hình file hosts và đưa vào file cấu hình **cluster**.
       
       - Sau khi cấu hình file hosts vào cluster xong. Các file này sẽ được chuyển đến các server có liên quan.
       
   - Start **cluster**
   
       ![image](https://user-images.githubusercontent.com/19284401/60791437-dce58200-a18d-11e9-8d88-23943e006e05.png)
       
       Chú ý: Phần password root sql đây là lý do vì sao mình nói các bạn nên đặt password sql root giống nhau. Mình sẽ thông qua ssh để gọi và thực gọi các lệnh sql trên các server mà ko cần nhập nhiều lần password.
       
       - Phần **info cluster** các bạn chú ý cho mình 1 vài điểm sau.
       
           ![image](https://user-images.githubusercontent.com/19284401/60792986-ee7c5900-a190-11e9-84d9-1067a3280208.png)
        
            - wsrep_local_statecomment : Trạng thái đồng bộ.
            
            - wsrep_incoming_addresses: Đầy là địa chỉ IP của các host trong group cluster, tuy nhiên ở đây mình ko đến gì nên nó hiện AUTO. Các bạn đọc ở phần tham khảo để biết thêm.
            
            - wsrep_cluster_size: Số lượng host sql có trong group cluster.
            
            - wsrep_connected: ON/OFF 
            
            - wsrep_ Provider_capabilities: Multi_Master
            
            - wsrep_ ready: ON/OFF
        

   - Tạo user xác thực cho HAproxy.
    
       ![image](https://user-images.githubusercontent.com/19284401/60793151-47e48800-a191-11e9-9d5c-c9affbad5c6e.png)
       
       - Test đồng bộ database 
       
       ![image](https://user-images.githubusercontent.com/19284401/60793616-3b146400-a192-11e9-940c-4a98b12576d7.png)
       
       - Việc cấu hình cluster đến đây là xong.
   
#### <a name=2.4><a/> 2.4 Cấu hình Max_scale 

   - ssh qua server Max_scale.

        ![image](https://user-images.githubusercontent.com/19284401/60793846-b2e28e80-a192-11e9-886f-74c4bdf3361f.png)
        
        - Cài đặt và cấu hình Max_scale.
        
                        python3.6 config_MaxScale.py                
        
        ![image](https://user-images.githubusercontent.com/19284401/60794007-05bc4600-a193-11e9-8cdc-d8551c806b8e.png)
        
        Chú ý: C ở đây ko phải là reboot server nữa nhé, tránh nhầm lần với những lần trước.
        
        - Sau khi cài đặt xong các bạn sẽ được yêu cầu nhập các thông tin như trong hình dưới. Để import vào file Max_scale.cnf
        
        ![image](https://user-images.githubusercontent.com/19284401/60795841-9c3e3680-a196-11e9-9cfa-f574208c69ac.png)
        
        - Vì 1 vài lý do nên mình ko sử dụng thư viện mysql của python. Các bạn thông cảm.
        
        - Sau khi cấu hình xong các bạn sẽ được kêt nối luôn vào mysql.
        
        ![image](https://user-images.githubusercontent.com/19284401/60797282-30110200-a199-11e9-9d4c-e3c2ef961dfc.png)
        
                    show variables like 'hostname';
                    
        ![image](https://user-images.githubusercontent.com/19284401/60797403-62226400-a199-11e9-8b02-775e47be1e41.png)
        
        - Host đang được gọi là **sql02**. Giờ ta sẽ test bằng cách stop sql trên host **sql02**, xem con Max_scale có tự động chuyển kết nối sang 2 host còn lại không.
        
                        systemctl stop mariadb
                        
                        systemctl status mariadb
        
        ![image](https://user-images.githubusercontent.com/19284401/60797602-c7765500-a199-11e9-8345-8fc81371270d.png)
        
        - Chạy lại lệnh sau.
            
                        show variables like 'hostname';
                        
        ![image](https://user-images.githubusercontent.com/19284401/60797728-0d331d80-a19a-11e9-99f8-28d704c57058.png)
        
        - Kết quả như trên có nghĩa là HAproxy đã hoạt đông ổn.
    
   - Như vậy là việc cấu hình Cluster và HAproxy Mariadb dựa trên **MariaDB Galera** và **MariaDB MaxScale** như vậy là xong. Bài viết của mình cũng xin dừng tại đây.
    
   - Chúc các bạn thành công.
                    
#### <a name=3><a/> III Tham khảo

- https://mariadb.com/resources/blog/getting-started-with-mariadb-galera-and-mariadb-maxscale-on-centos/

- https://viblo.asia/p/cai-dat-ha-galera-cluster-mariadb-su-dung-maxscale-tren-centos-6-ZDEvLRaEeJb

- https://www.debyum.com/setup-mariadb-galera-cluster-in-centos-7/

- http://www.techbrothersit.com/2018/06/how-to-create-galera-cluster-with.html

                
#### <a name=3.1><a/>3.1 Liên hệ


<a href="https://www.facebook.com/trunglv.91" rel="nofollow">Facebook<a>

  


    

   
                   
                    
  


   

   
   

                     
        
        
    
        

                 
        
        





