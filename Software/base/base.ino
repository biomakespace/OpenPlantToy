
#include <stdio.h>

using namespace std;

#include <SoftwareSerial.h>

#define SOFTWARE_SERIAL_TX      2
#define SOFTWARE_SERIAL_RX      3
                                  
#define BAUD_RATE               4800
                                    
#define RESET_LIGHT_PIN         13

#define BUFFER_SIZE             128

#define MESSAGE_TERMINATOR      ';'

// Create software serial object
SoftwareSerial upstreamSerial(SOFTWARE_SERIAL_RX, SOFTWARE_SERIAL_TX);

// Node to use in linked list

template <typename T>
class Node {
  private:
    T data;
    Node* next;
   public:
    Node(T newData);
    Node* getNext();
    void setNext(Node* newNext);
    T getData();
};

// Constructor
template <typename T>
Node<T>::Node(T newData) {
  data = newData; 
}

// Setters/getters
template <typename T>
Node<T>* Node<T>::getNext() {
  return next;
}

template <typename T>
void Node<T>::setNext(Node* newNext) {
  next = newNext;
}

template <typename T>
T Node<T>::getData() {
  return data;
}

//

// Linked List class

template <typename T>
class LinkedList {
  private:
    Node<T>* head;
    int length;
   public:
    LinkedList();
    Node<T>* bringMeHisHead();
    void push(Node<T>* newTail);
    void offWithHisHead();
    void offWithHisHeads(int heads);
};

template <typename T>
LinkedList<T>::LinkedList() {
  length = 0;
}

// peek at the head node
template <typename T>
Node<T>* LinkedList<T>::bringMeHisHead() {
  return head;
}

// Add a node to the end
template <typename T>
void LinkedList<T>::push(Node<T>* newTail) {
  // For an empty list, this becomes the head
  if (length == 0) {
    head = newTail;
  } else {
    /*  
     * Walk the list to the end 
     * Note that since we start at element
     * 1 with the head, we only need to
     * make length - 1 hops
     */
    Node<T>* currentNode = head;
    for(int i=0; i<(length-1); i++) {  
      currentNode = currentNode->getNext();
    }
    // Set the new tail as the last element's next
    currentNode->setNext(newTail);
    // LinkedList grew by one!
    length++;
  }
  
}

// Throw away the first node (don't return it)
template <typename T>
void LinkedList<T>::offWithHisHead() {
  if (length > 0) {
    Node<T>* deleteMe = head;
    head = head->getNext();
    delete deleteMe;
    length--;
  }
}

// Throw away the first n nodes
template <typename T>
void LinkedList<T>::offWithHisHeads(int heads) {
  for(int i=0; i<heads; i++) {
    offWithHisHead();
  }
}

// Buffers (linked lists of bytes)
LinkedList<char>* downstreamBuffer = new LinkedList<char>();
LinkedList<char>* upstreamBuffer = new LinkedList<char>();

void setup() {
  Serial.begin(BAUD_RATE);
  while(!Serial) {
    // Wait to serial to start up
  }
  upstreamSerial.begin(BAUD_RATE);
}

void loop() {
  // put your main code here, to run repeatedly:

}
