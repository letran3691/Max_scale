## Max_scale

Getting Started with MariaDB Galera and MariaDB MaxScale on CentOS 7.x

## Mục lục

---------------------------------------------

### [I Giới thiệu](#I)
- [1. Mariadeb](#1)
- [2 Galera Cluster](#2)
- [2MariaDB MaxScale](#3)

#### [II. Cài đặt](#2)
- [2.1 Cài đặt python3.6](#2.1)
- [2.2 Cài đặt-cấu hình domain](#2.2)
- [2.3 Test đồng bộ](#2.3)
- [2.4 Cấu hình DNS](#2.4)
#### [3 Tham khảo](#3)
- [3.1 Liên hệ](#3.1)


###<a name="I"></a>I. Giới thiệu


#####<a name="1"></a>1 MariaDB.
    
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

#####<a name="2"></a>2. Galera Cluster.

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
       
#####<a name="3"></a>3. MariaDB MaxScale.

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

