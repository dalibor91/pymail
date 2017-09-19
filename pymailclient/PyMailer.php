<?php 

/**
 * PHP Class for using pymail 
 * @author Dalibor Menkovic <dalibor.menkovic@gmail.com>
 */

class PyMailer {
  
  /**
   * Array with email options
   * @var array
   */
  protected $email = [];
  
  //construct 
  public function __construct($from) {
    $this->_resetMail();
    $this->setFrom($from);
  }
  
  /**
   * Sets From option in email 
   * @access public 
   * @param string $from - email 
   * @return self
   */
  public function setFrom($from){
    $this->email['from'] = trim(strval($from));
    return $this;
  }
  
  /**
   * Sets Subject of email
   * @access public 
   * @param string $s - subject 
   * @return self
   */
  public function setSubject($s) {
    $this->email['subject'] = trim(strval($s));
    return $this;
  }
  
  /**
   * Sets Content of email
   * @access public 
   * @param string $b - body 
   * @return self
   */
  public function setBody($b) {
    $this->email['body'] = trim(strval($b));
    return $this;
  }
  
  /**
   * Sets To of email
   * @access public 
   * @param string $toEmail - To email
   * @param string $toName - name of person - default null 
   * @return self
   */
  public function addTo($toEmail, $toName= null) {
    $this->email['recieve']['to'][] = [
      'email' => $toEmail, 
      'name' => $toName
    ];
    
    return $this;
  }
  
  /**
   * Sets CC of email
   * @access public 
   * @param string $toEmail - To email
   * @param string $toName - name of person - default null 
   * @return self
   */
  public function addCC($toEmail, $toName= null) {
    $this->email['recieve']['cc'][] = [
      'email' => $toEmail, 
      'name' => $toName
    ];
    
    return $this;
  }
  
  /**
   * Sets BCC of email
   * @access public 
   * @param string $toEmail - To email
   * @param string $toName - name of person - default null 
   * @return self
   */
  public function addBCC($toEmail, $toName= null) {
    $this->email['recieve']['bcc'][] = [
      'email' => $toEmail, 
      'name' => $toName
    ];
    
    return $this;
  }
  
  /**
   * Adds attachement to email 
   * @access public 
   * @param string $file - path to file 
   * @throws Exception
   * @return self
   */
  public function attach($file) {
    
    if (!file_exists($file)){
      throw new Exception("File {$file} does not exists");
    }
    
    $this->email['attach'][] = [
      'name' => basename($file), 
      'content' => base64_encode(file_get_contents($file))
    ];
    
    return $this;
  }
  
  /**
   * Sends out built email  
   * @access public 
   * @param string $host - host where server is located 
   * @param int $port - port of the server 
   * @param string $login - login string - "username:password"
   * @throws Exception
   * @return self
   */
  public function send($host, $port='', $login='') {
    
    $this->validate();
    
    $port = !empty($port) ? ":{$port}" : "";
    $url = "http://{$host}{$port}/send";
    
    $ch = curl_init();

    curl_setopt($ch, CURLOPT_URL,$url);
    curl_setopt($ch, CURLOPT_POST, 1);
    curl_setopt($ch, CURLOPT_POSTFIELDS,json_encode($this->email));
    
    $headers = [
      'Content-Type: application/json'
    ];
    
    if (!empty($login)) {
      $headers[] = sprintf('Authorization: Basic %s', base64_encode($login));
    }
    
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $u = curl_exec ($ch);
    curl_close($ch);
    $data = json_decode($u, true);

    return isset($data['success']) && ($data['success'] === true);
  }
  
  /**
   * Clears build email
   * @access public 
   * @return self
   */
  public function clear() {
    $this->_resetMail();
    return $this;
  }
  
  /**
   * Clears build email array
   * @access private 
   * @return null
   */
  private function _resetMail(){
    $this->email = [
      'from' => null, 
      'recieve' => [
        'to' => [], 
        'cc' => [], 
        'bcc' => []
      ], 
      'subject' => null, 
      'body' => null, 
      'attach' => []
    ];
  }
  
  /**
   * Validates build email 
   * @access private 
   * @throws Exception
   * @return null
   */
  private function validate() {
    if (empty($this->email['recieve']['to'])) {
      throw new Exception("Must have reciever");
    } 
    
    if (empty($this->email['from'])) {
      throw new Exception("Must have from");
    } 
    
    if (empty($this->email['subject'])) {
      throw new Exception("Must have subject");
    } 
    
    if (empty($this->email['body'])) {
      throw new Exception("Must have body");
    } 
  }
}

