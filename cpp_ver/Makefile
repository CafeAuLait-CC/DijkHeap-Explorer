CXX := g++
CXXFLAGS := -std=c++17 -O3 -Wall -Wextra -Iinclude
LDFLAGS := 
TARGET := dijkstra

# Source files
SRC_DIR := src
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(patsubst $(SRC_DIR)/%.cpp,obj/%.o,$(SRCS))

# Header files
INC_DIR := include
INCLUDES := -I$(INC_DIR)

# JSON library (header-only)
JSON_INC := -I./include/json.hpp

.PHONY: all clean

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(JSON_INC) $^ -o $@ $(LDFLAGS)

obj/%.o: $(SRC_DIR)/%.cpp | obj
	$(CXX) $(CXXFLAGS) $(INCLUDES) $(JSON_INC) -c $< -o $@

obj:
	mkdir -p obj

clean:
	rm -rf obj $(TARGET)